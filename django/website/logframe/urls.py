from django.conf.urls import patterns, url
from .views import ResultEditor, ResultMonitor


urlpatterns = patterns('',
    url(r'^design/(?P<logframe_id>\d+)/result/(?P<pk>\d+)/$',
        ResultEditor.as_view(),
        name="design-result"),
    url(r'^monitor/(?P<logframe_id>\d+)/result/(?P<pk>\d+)/$',
        ResultMonitor.as_view(),
        name="monitor-result"),
)
