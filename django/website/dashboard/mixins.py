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
