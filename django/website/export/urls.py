from django.conf.urls import patterns, url
from .views import ExportLogframeData, ExportAnnualPlan, ExportQuarterPlan


urlpatterns = patterns('',
    url(r'^data/(?P<pk>\d+)/(?P<period>\d{4}-\d{2}-\d{2})/$',
        ExportLogframeData.as_view(),
        name="export-logframe-data-period"),
    url(r'^data/(?P<pk>\d+)/quarterly-plan/(?P<month>\d{2})-(?P<year>\d{4})/$',
        ExportQuarterPlan.as_view(),
        name="export-quarter-plan"),
    url(r'^data/(?P<pk>\d+)/annual-plan/(?P<year>\d{4})/$',
        ExportAnnualPlan.as_view(),
        name="export-annual-plan"),
)
