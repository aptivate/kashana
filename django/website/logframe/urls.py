from django.conf.urls import url
from .views import CreateLogframe, ResultEditor, ResultMonitor


urlpatterns = [
    url(r'^design/(?P<logframe_id>\d+)/result/(?P<pk>\d+)/$',
        ResultEditor.as_view(),
        name="design-result"),
    url(r'^monitor/(?P<logframe_id>\d+)/result/(?P<pk>\d+)/$',
        ResultMonitor.as_view(),
        name="monitor-result"),
    url(r'^create/', CreateLogframe.as_view(), name='create-logframe'),
]
