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


def update_current_logframe(user, logframe):
    user.last_viewed_logframe = logframe
    user.save()


class OverviewMixin(object):
    def get_logframe(self):
        if not LogFrame.objects.exists():
            LogFrame.objects.create(name=settings.DEFAULT_LOGFRAME_NAME, slug=settings.DEFAULT_LOGFRAME_SLUG)

        user = self.request.user

        if 'slug' in self.kwargs or user.last_viewed_logframe:
            slug = self.kwargs.get('slug') or user.last_viewed_logframe.slug

            if not user.last_viewed_logframe or slug != user.last_viewed_logframe.slug:
                logframe = get_object_or_404(LogFrame, slug=slug)
                update_current_logframe(user, logframe)
            else:
                logframe = user.last_viewed_logframe

        else:
            logframe = LogFrame.objects.all().order_by('id')[0]
            update_current_logframe(user, logframe)

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
