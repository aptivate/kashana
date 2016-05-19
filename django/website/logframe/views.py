import re
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django_tables2.views import SingleTableView
from .models import (
    Assumption, Indicator, LogFrame, Milestone, Result, RiskRating,
    SubIndicator, Target
)
from .api import ResultSerializer
from .mixins import AptivateDataBaseMixin
from .tables import LogframeManagementTable


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


class CreateLogframe(PermissionRequiredMixin, CreateView):
    model = LogFrame
    fields = ['name']
    template_name = 'logframe/edit_logframe.html'
    permission_required = 'logframe.edit_logframe'

    def get_unique_slug_name(self, logframe):
        slug = logframe.name.lower()
        slug = slug.replace(' ', '_')
        slug = re.sub('[^\w-]', '', slug)
        slug = slug[:46]
        if LogFrame.objects.filter(slug=slug).exists():
            count = LogFrame.objects.filter(slug__startswith=slug).count() + 1
            slug += unicode(count)
        return slug

    def get_success_url(self):
        return reverse('manage-logframes')

    def form_valid(self, form):
        form.instance.slug = self.get_unique_slug_name(form.instance)
        return CreateView.form_valid(self, form)


class ManageLogframes(PermissionRequiredMixin, SingleTableView):
    permission_required = 'logframe.edit_logframe'
    model = LogFrame
    table_class = LogframeManagementTable

    def get_table(self, **kwargs):
        table = SingleTableView.get_table(self, **kwargs)
        if len(table.data) == 1:
            table.exclude = ('delete',)
        return table


class EditLogframe(PermissionRequiredMixin, UpdateView):
    model = LogFrame
    fields = ['name', 'slug']
    template_name = 'logframe/edit_logframe.html'
    permission_required = 'logframe.edit_logframe'

    def get_success_url(self):
        return reverse('manage-logframes')


class DeleteLogframe(PermissionRequiredMixin, DeleteView):
    model = LogFrame
    permission_required = 'logframe.edit_logframe'

    def get_success_url(self):
        return reverse('manage-logframes')
