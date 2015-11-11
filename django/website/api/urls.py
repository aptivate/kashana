from django.conf.urls import (
    include,
    url
)
from logframe.api import (
    router,
)

# URLs
urlpatterns = [
    url(r'^', include(router.urls)),
]
