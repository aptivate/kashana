from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from logframe.mixins import AptivateDataBaseMixin
from .mixins import OverviewMixin


class Home(OverviewMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'

    def get(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            return HttpResponseRedirect("{0}?next={1}".format(reverse("login"),
                                                              reverse("home")))
        return HttpResponseRedirect(reverse(u"dashboard"))


class DashboardView(LoginRequiredMixin,
                    OverviewMixin, AptivateDataBaseMixin, TemplateView):
    template_name = 'dashboard/dashboard_base.html'
