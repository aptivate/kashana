from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from logframe.mixins import AptivateDataBaseMixin
from logframe.models import LogFrame
from .mixins import OverviewMixin, update_last_viewed_logframe


class Home(LoginRequiredMixin, OverviewMixin, RedirectView):
    permanent = False
    pattern_name = 'dashboard'


class DashboardView(LoginRequiredMixin,
                    OverviewMixin, AptivateDataBaseMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'


class SwitchLogframes(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = 'logframe-dashboard'

    def post(self, request, *args, **kwargs):
        try:
            self.object = LogFrame.objects.get(pk=self.request.POST['logframe'])
            update_last_viewed_logframe(self.request.user, self.object)
            response = self.get(request, slug=self.object.slug)
        except LogFrame.DoesNotExist:
            self.pattern_name = 'create-logframe'
            response = self.get(request)
        return response


class DashboardLogframeSelection(LoginRequiredMixin, ListView):
    model = LogFrame
    context_object_name = 'logframe_list'
    template_name = 'dashboard/dashboard_logframe_list.html'
