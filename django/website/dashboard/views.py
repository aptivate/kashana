from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from logframe.models import (
    LogFrame,
    Activity,
    BudgetLine,
    TALine,
    StatusUpdate,
    TAType,
    StatusCode,
)
from logframe.mixins import AptivateDataBaseMixin


class OverviewMixin(object):
    def get_logframe(self):
        return LogFrame.objects.get_or_create()[0]

    def get_activities(self, logframe):
        return self.get_related_model_data(
            {'log_frame': logframe}, Activity)

    def get_activities_data(self, logframe, model):
        return self.get_related_model_data(
            {'activity__log_frame': logframe}, model)

    def get_data(self, logframe, data):
        data.update({
            'export_url': reverse("export-logframe-data-period",
                                  args=[logframe.id, "1900-01-01"]),
            'activities': self.get_activities(logframe),
            'tatypes': [{"id": t.id, "name": t.name}
                        for t in TAType.objects.filter(log_frame=logframe)],
            'statuscodes': [{"id": c.id, "name": c.name}
                            for c in StatusCode.objects.filter(
                                log_frame=logframe)],
            'budgetlines': self.get_activities_data(logframe, BudgetLine),
            'talines': self.get_activities_data(logframe, TALine),
            'statusupdates': self.get_activities_data(logframe, StatusUpdate)
        })
        return data


class Home(TemplateView):
    template_name = 'dashboard/dashboard_base.html'

    def get(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            return HttpResponseRedirect("{0}?next={1}".format(reverse("login"),
                                                              reverse("home")))
        return HttpResponseRedirect(reverse(u"dashboard"))


class DashboardView(LoginRequiredMixin,
                    OverviewMixin, AptivateDataBaseMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'
