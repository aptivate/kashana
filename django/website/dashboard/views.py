from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from logframe.mixins import AptivateDataBaseMixin
from .mixins import OverviewMixin


class Home(LoginRequiredMixin, OverviewMixin, RedirectView):
    permanent = False
    pattern_name = 'dashboard'


class DashboardView(LoginRequiredMixin,
                    OverviewMixin, AptivateDataBaseMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'
