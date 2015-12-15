from django.core.urlresolvers import reverse

from logframe.models import (
    LogFrame,
    Activity,
    TAType,
    StatusCode,
    BudgetLine,
    TALine,
    StatusUpdate
)
from django.conf import settings
from django.shortcuts import get_object_or_404


class OverviewMixin(object):
    def get_logframe(self):
        if not LogFrame.objects.exists():
            LogFrame.objects.create(name=settings.DEFAULT_LOGFRAME_NAME)

        if 'slug' in self.kwargs or 'current_logframe' in self.request.session:
            slug = self.kwargs.get('slug') or self.request.session['current_logframe']
            logframe = get_object_or_404(LogFrame, slug=slug)
            if 'current_logframe' not in self.request.session or slug != self.request.session['current_logframe']:
                self.request.session['current_logframe'] = slug
        else:
            logframe = LogFrame.objects.all().order_by('id')[0]
            self.request.session['current_logframe'] = logframe.slug

        return logframe

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
            'export_annual_plan_url': reverse(
                "export-annual-plan", args=[logframe.id, "1900"]),
            'export_quarter_plan_url': reverse(
                "export-quarter-plan", args=[logframe.id, "01", "1900"]),
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
