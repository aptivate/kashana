from django.conf.urls import (
    patterns,
    include,
    url
)
from logframe.api import (
    router,
)

# URLs
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
