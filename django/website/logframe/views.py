from django.views.generic import DetailView
from braces.views import LoginRequiredMixin
from .models import (
    Result, Assumption, Indicator, SubIndicator, Target, Milestone, RiskRating
)
from .api import ResultSerializer
from .mixins import AptivateDataBaseMixin


class ResultEditor(LoginRequiredMixin, AptivateDataBaseMixin, DetailView):
    model = Result
    template_name = 'logframe/result.html'

    def get_logframe(self):
        return self.object.log_frame

    def get_data(self, logframe, data):
        """
        Get a dict containing all the data for one logframe
        """
        result = self.object
        data.update({
            'result': ResultSerializer(result).data,
            'riskratings': self._json_object_list(
                RiskRating.objects.all(),
                model_class=RiskRating),
            'assumptions': self._json_object_list(
                logframe.all_assumptions(),
                model_class=Assumption),
            'indicators': self.get_related_model_data(
                {'result': result},
                Indicator),
            'subindicators': self.get_related_model_data(
                {'indicator__result': result},
                SubIndicator),
            'targets': self.get_related_model_data(
                {'subindicator__indicator__result': result},
                Target),
            'milestones': self.get_related_model_data(
                {'log_frame': result.log_frame},
                Milestone),
        })
        return data


class ResultMonitor(LoginRequiredMixin, AptivateDataBaseMixin, DetailView):
    model = Result
    template_name = 'logframe/result.html'

    def get_logframe(self):
        return self.object.log_frame

    def get_data(self, logframe, data):
        """
        Get a dict containing all the data for one logframe
        """
        data.update({
            'result': ResultSerializer(self.object).data,
        })
        return data
