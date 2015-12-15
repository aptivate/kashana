from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import UpdateView

from braces.views import LoginRequiredMixin

from logframe.mixins import AptivateDataBaseMixin
from logframe.models import LogFrame
from .mixins import OverviewMixin
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404


class Home(LoginRequiredMixin, OverviewMixin, RedirectView):
    permanent = False
    pattern_name = 'dashboard'


class DashboardView(LoginRequiredMixin,
                    OverviewMixin, AptivateDataBaseMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'


class SwitchLogframes(RedirectView):
    permanent = False
    pattern_name = 'logframe-dashboard'

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(LogFrame, pk=self.request.POST['id'])
        return self.get(request, slug=self.object.slug)
