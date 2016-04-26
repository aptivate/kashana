from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView
from braces.views import LoginRequiredMixin
from .models import (
    Assumption, Indicator, LogFrame, Milestone, Result, RiskRating,
    SubIndicator, Target
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


class CreateLogframe(LoginRequiredMixin, CreateView):
    model = LogFrame
    fields = ['name', 'slug']
    template_name = 'logframe/create_logframe.html'

    def get_success_url(self):
        return reverse('logframe-dashboard', kwargs={'slug': self.object.slug})
