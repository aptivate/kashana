from rest_framework import viewsets, serializers, filters, permissions
from rest_framework_nested import routers
import django_filters
from logframe import models


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
        ids = [int(i) for i in request.QUERY_PARAMS.getlist('id')]
        if len(ids):
            return queryset.filter(id__in=ids)
        return queryset


class FilterRelationship(object):
    filter_backends = (IDFilterBackend,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          CanEditOrReadOnly)

    def get_queryset(self):
        relationship = {self.lookup_rel: self.kwargs['logframe_pk']}
        return self.model.objects.filter(**relationship)


#
# Serializers & ViewSets
#

# Logframe
class LogFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogFrame
        fields = ('id', 'name', 'results')


class LogFrameViewSet(viewsets.ModelViewSet):
    model = models.LogFrame
    serializer_class = LogFrameSerializer


# Results
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
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
    model = models.Result
    serializer_class = ResultSerializer
    lookup_rel = 'log_frame_id'


# Indicators & subindicators
class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Indicator
        fields = (
            'id',
            'name',
            'description',
            'result',
            'source',
            'subindicators',
        )


class IndicatorViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Indicator
    serializer_class = IndicatorSerializer
    lookup_rel = 'result__log_frame_id'


class SubIndicatorFilter(django_filters.FilterSet):
    result = django_filters.NumberFilter(name='indicator__result_id')

    class Meta:
        model = models.SubIndicator
        fields = ['result']


class SubIndicatorViewSet(viewsets.ModelViewSet):
    model = models.SubIndicator
    lookup_rel = 'indicator__result__log_frame_id'


# Milestones
class MilestoneViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Milestone
    lookup_rel = 'log_frame_id'


# Targets
class TargetFilter(django_filters.FilterSet):
    result = django_filters.NumberFilter(name='subindicator__indicator__result_id')

    class Meta:
        model = models.Target
        fields = ['result']


class TargetViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Target
    lookup_rel = 'milestone__log_frame_id'
    filter_backends = (filters.DjangoFilterBackend, IDFilterBackend)
    filter_class = TargetFilter


class ActualViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Actual
    lookup_rel = 'indicator__result__log_frame_id'


class ColumnViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Column
    lookup_rel = 'indicator__result__log_frame_id'

    def get_queryset(self):
        qs = super(ColumnViewSet, self).get_queryset()
        return qs.order_by('date', 'id')


# RiskRatings
class RiskRatingViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.RiskRating
    lookup_rel = 'result__log_frame_id'


# Assumptions
class AssumptionViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Assumption
    lookup_rel = 'result__log_frame_id'


# Activities
class ActivityViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Activity
    lookup_rel = 'log_frame_id'


class BudgetLineViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.BudgetLine
    lookup_rel = 'activity__log_frame_id'


class TALinesViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.TALine
    lookup_rel = 'activity__log_frame_id'


class TATypeViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.TAType
    lookup_rel = 'log_frame_id'


class StatusCodeViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.StatusCode
    lookup_rel = 'log_frame_id'


class StatusUpdateSerializer(serializers.ModelSerializer):

    user_id = serializers.Field(source='user.id')

    def validate_user(self, attrs, source):
        return attrs

    class Meta:
        model = models.StatusUpdate
        exclude = ('user',)


class StatusUpdateViewSet(FilterRelationship, viewsets.ModelViewSet):
    lookup_rel = 'activity__log_frame_id'
    serializer_class = StatusUpdateSerializer
    model = models.StatusUpdate

    def get_queryset(self):
        qs = super(StatusUpdateViewSet, self).get_queryset()
        return qs.order_by('date', 'id')

    def pre_save(self, status_update):
        status_update.user = self.request.user


# Ratings
class RatingViewSet(FilterRelationship, viewsets.ModelViewSet):
    model = models.Rating
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
