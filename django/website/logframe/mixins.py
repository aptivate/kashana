from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer
from contacts.models import User
from appconf.models import Settings
from .api import (
    LogFrameSerializer,
    ResultSerializer,
    SettingsSerializer,
    create_serializer
)
from .models import Period, Rating, ResultLevelName


class QuerysetSerializer(object):
    create_serializer = staticmethod(create_serializer)

    @staticmethod
    def _json_object_list(qs, serializer=None, model_class=None):
        """
        Serialize a queryset to a list of json objects
        using the given serializer
        """
        if serializer is None:
            serializer = QuerysetSerializer.create_serializer(model_class)
        return [serializer(o).data for o in qs.all()]


class AptivateDataBaseMixin(QuerysetSerializer):
    def is_editable(self):
        editable = False
        if hasattr(self, "request") and hasattr(self.request, "user") \
                and self.request.user.has_perm:
            editable = self.request.user.has_perm('contacts.edit_logframe')
        return editable

    def get_related_model_data(self, filter_dict, model):
        instances = model.objects.filter(**filter_dict)
        return self._json_object_list(instances, None, model)

    def get_settings(self, logframe):
        serializer = SettingsSerializer
        conf = Settings.objects.get_or_create(logframe=logframe)[0]
        serialized = serializer(conf).data
        del serialized['id']
        return serialized

    def get_periods(self, logframe):
        # Get periods from the oldest milestone (start) to the most recent
        # entry (end); or should that be last milestone?
        periods = []
        milestones = list(logframe.milestones)
        period, created = Period.objects.get_or_create(log_frame=logframe)
        if len(milestones):
            periods = period.get_periods(milestones[0].date,
                                         milestones[-1].date)
        return periods

    def get_logframe_data(self, logframe):
        """
        Get a dict containing all the data commonly shared by all parts
        of the app
        """
        data = {
            'logframe': LogFrameSerializer(logframe).data,
            'levels': {
                the_level_name.level_number: the_level_name.level_name
                for the_level_name in ResultLevelName.objects.all()
            },
            'ratings': self.get_related_model_data(
                {'log_frame': logframe}, Rating),
            'results': self._json_object_list(logframe.results,
                                              ResultSerializer),
            'users': [{"id": u.id, "name": u.get_full_name()}
                      for u in User.objects.filter(organizations_organization=logframe.organization)],
            'periods': self.get_periods(logframe),
            'conf': self.get_settings(logframe),
            'is_editable': self.is_editable()
        }
        return data

    def get_context_data(self, **kwargs):
        ctx = super(AptivateDataBaseMixin, self).get_context_data(**kwargs)
        lf = self.get_logframe()
        data = self.get_logframe_data(lf)
        ctx['data'] = JSONRenderer().render(self.get_data(lf, data))
        return ctx
