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
from organizations.models import Organization


def update_last_viewed_item(user, item):
    setattr(user.preferences, 'last_viewed_' + item.__class__.__name__.lower(), item)
    user.preferences.save()


class OverviewMixin(object):
    def get_item(self, klass, slug_field_name, **item_kwargs):
        user = self.request.user
        if not klass.objects.exists():
            item = klass.objects.create(**item_kwargs)
            if hasattr(item, 'add_user'):
                item.add_user(user)
        item = getattr(user.preferences, 'last_viewed_' + klass.__name__.lower())

        if slug_field_name in self.kwargs or item:
            slug = self.kwargs.get(slug_field_name) or item.slug

            if not item or slug != item.slug:
                new_item = get_object_or_404(klass, slug=slug)
                update_last_viewed_item(user, new_item)
            else:
                new_item = item
        else:
            new_item = klass()
        return new_item

    def get_organization(self):
        organization = self.get_item(Organization, 'org_slug', name=settings.DEFAULT_ORGANIZATION_NAME)
        if not organization.pk:
            if self.request.user.organizations_organization.exists():
                organization = self.request.user.organizations_organization.first()
            update_last_viewed_item(self.request.user, organization)

        return organization

    def get_logframe(self):
        organization = self.get_organization()
        logframe = self.get_item(LogFrame, 'slug',
                name=settings.DEFAULT_LOGFRAME_NAME,
                slug=settings.DEFAULT_LOGFRAME_SLUG,
                organization=organization)

        if not logframe.pk:
            logframe = LogFrame.objects.filter(organization=organization).order_by('id')[0]
            update_last_viewed_item(self.request.user, logframe)

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
