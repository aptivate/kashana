import json

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import Http404

import django_filters

from rest_framework import viewsets, serializers, filters, permissions
from rest_framework.response import Response
from rest_framework.serializers import (
    ManyRelatedField, ModelSerializer, PrimaryKeyRelatedField
)
from rest_framework.views import APIView
from rest_framework_nested import routers

from .models import (
    Activity, Actual, Assumption, BudgetLine, Column, Indicator, LogFrame,
    Milestone, Rating, Result, RiskRating, StatusCode, StatusUpdate,
    SubIndicator, TALine, TAType, Target
)


def create_serializer(model_class):
        assert model_class is not None

        class DefaultSerializer(ModelSerializer):
            class Meta:
                model = model_class
        return DefaultSerializer


#
# Mixins
#
class CanEditOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return request.user.has_perm('contacts.edit_logframe')


class IDFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ids = [int(i) for i in request.query_params.getlist('id')]
        if len(ids):
            return queryset.filter(id__in=ids)
        return queryset


#
#  Time period filter
#
def build_period_filter(start_date, end_date, s_lookup, e_lookup):
    '''
          x|---------1---------|y
    <----2-----|y
                          x|-----3---->
    <-4--|y
               x|----5---|y
         x|----6---|y
                       x|----7---|y
    <---------------8----------------->
                                x|-9-->
             s               e
    ---------|---------------|---------

    Correct matches:
        1) x >= s & x <= e      [3, 5, 7]
        2) x <= s & y >= s      [1, 2, 6]

        3) x <= e & y is None (no end date)
        4) y >= s & x is None (no start date)

        5) x & y both None      [8]

    assumptions: x < y, s < e

    '''
    s_gte = s_lookup + "__gte"
    s_lte = s_lookup + "__lte"
    e_gte = e_lookup + "__gte"

    rel_1 = Q(**{s_gte: start_date}) & Q(**{s_lte: end_date})
    rel_2 = Q(**{s_lte: start_date}) & Q(**{e_gte: start_date})
    rel_3 = Q(**{s_lte: end_date}) & Q(**{e_lookup: None})
    rel_4 = Q(**{e_gte: start_date}) & Q(**{s_lookup: None})
    rel_5 = Q(**{s_lookup: None}) & Q(**{e_lookup: None})
    return rel_1 | rel_2 | rel_3 | rel_4 | rel_5


def get_period_filter(start_date, end_date, s_lookup, e_lookup):
    def curried(queryset):
        if start_date and end_date:
            queryset = queryset.filter(build_period_filter(
                start_date, end_date, s_lookup, e_lookup))
        return queryset
    return curried


class PeriodOverlapFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        s_lookup = view.lookup_period_start
        e_lookup = view.lookup_period_end

        filter_func = get_period_filter(start_date, end_date, s_lookup, e_lookup)
        return filter_func(queryset)


class FilterRelationship(object):
    filter_backends = (IDFilterBackend,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          CanEditOrReadOnly)

    def get_queryset(self):
        relationship = {self.lookup_rel: self.kwargs['logframe_pk']}
        return self.queryset.filter(**relationship)


#
# Serializers & ViewSets
#

# Logframe
class LogFrameSerializer(ModelSerializer):
    class Meta:
        model = LogFrame
        fields = ('id', 'name', 'results')


class LogFrameViewSet(viewsets.ModelViewSet):
    queryset = LogFrame.objects.all()
    serializer_class = LogFrameSerializer


class SwitchLogframes(APIView):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not LogFrame.objects.filter(pk=request.data['new_logframe_id']).exists():
            raise Http404
        request.session['current_logframe'] = request.data['new_logframe_id']
        response_data = json.dumps({'redirect': reverse('dashboard')})
        return Response(response_data)


# Results
class ResultSerializer(ModelSerializer):
    indicators = ManyRelatedField(child_relation=PrimaryKeyRelatedField(queryset=Indicator.objects.all()), required=False)
    activities = ManyRelatedField(child_relation=PrimaryKeyRelatedField(queryset=Activity.objects.all()), required=False)
    assumptions = ManyRelatedField(child_relation=PrimaryKeyRelatedField(queryset=Assumption.objects.all()), required=False)

    class Meta:
        model = Result
        fields = (
            'id',
            'name',
            'description',
            'order',
            'parent',
            'level',
            'contribution_weighting',
            'risk_rating',
            'rating',
            'log_frame',
            'indicators',
            'activities',
            'assumptions'
        )


class ResultViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_rel = 'log_frame_id'


# Indicators & subindicators
class IndicatorSerializer(ModelSerializer):
    subindicators = ManyRelatedField(child_relation=PrimaryKeyRelatedField(queryset=SubIndicator.objects.all()), required=False)

    class Meta:
        model = Indicator
        fields = (
            'id',
            'name',
            'description',
            'result',
            'source',
            'subindicators',
        )


class IndicatorViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    lookup_rel = 'result__log_frame_id'


class SubIndicatorViewSet(viewsets.ModelViewSet):
    queryset = SubIndicator.objects.all()
    lookup_rel = 'indicator__result__log_frame_id'
    serializer_class = create_serializer(queryset.model)


# Milestones
class MilestoneViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    lookup_rel = 'log_frame_id'
    serializer_class = create_serializer(queryset.model)


# Targets
class TargetFilter(django_filters.FilterSet):
    result = django_filters.NumberFilter(name='subindicator__indicator__result_id')

    class Meta:
        model = Target
        fields = ['result']


class TargetViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'milestone__log_frame_id'
    filter_backends = (filters.DjangoFilterBackend, IDFilterBackend)
    filter_class = TargetFilter


class ActualViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Actual.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'indicator__result__log_frame_id'


class ColumnViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'indicator__result__log_frame_id'

    def get_queryset(self):
        qs = super(ColumnViewSet, self).get_queryset()
        return qs.order_by('date', 'id')


# RiskRatings
class RiskRatingViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = RiskRating.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'result__log_frame_id'


# Assumptions
class AssumptionViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Assumption.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'result__log_frame_id'


# Activities
class ActivityViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'log_frame_id'
    lookup_period_start = 'start_date'
    lookup_period_end = 'end_date'
    filter_backends = (PeriodOverlapFilterBackend, IDFilterBackend)


# Budgetlines
class BudgetLineViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = BudgetLine.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'activity__log_frame_id'
    lookup_period_start = 'activity__start_date'
    lookup_period_end = 'activity__end_date'
    filter_backends = (PeriodOverlapFilterBackend, IDFilterBackend)


# TAs
class TALinesViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = TALine.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'activity__log_frame_id'
    lookup_period_start = 'activity__start_date'
    lookup_period_end = 'activity__end_date'
    filter_backends = (PeriodOverlapFilterBackend, IDFilterBackend)


class TATypeViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = TAType.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'log_frame_id'


# Statuses
class StatusCodeViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = StatusCode.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'log_frame_id'


# StatusUpdate
class StatusUpdateSerializer(ModelSerializer):

    user = serializers.Field(source='user.id')

    class Meta:
        model = StatusUpdate


class StatusUpdateViewSet(FilterRelationship, viewsets.ModelViewSet):
    lookup_rel = 'activity__log_frame_id'
    serializer_class = StatusUpdateSerializer
    queryset = StatusUpdate.objects.all()
    lookup_period_start = 'activity__start_date'
    lookup_period_end = 'activity__end_date'
    filter_backends = (PeriodOverlapFilterBackend, IDFilterBackend)

    def get_queryset(self):
        qs = super(StatusUpdateViewSet, self).get_queryset()
        return qs.order_by('date', 'id')

    def pre_save(self, status_update):
        status_update.user = self.request.user


# Ratings
class RatingViewSet(FilterRelationship, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = create_serializer(queryset.model)
    lookup_rel = 'log_frame_id'


# Routers
# Top level router
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'logframes', LogFrameViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/riskratings', RiskRatingViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/results', ResultViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/milestones', MilestoneViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/ratings', RatingViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/tatypes', TATypeViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/indicators', IndicatorViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/assumptions', AssumptionViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/activities', ActivityViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/columns', ColumnViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/targets', TargetViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/actuals', ActualViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/subindicators', SubIndicatorViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/budgetlines', BudgetLineViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/talines', TALinesViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/statuscodes', StatusCodeViewSet)
router.register(r'logframes/(?P<logframe_pk>.+)/statusupdates', StatusUpdateViewSet)
