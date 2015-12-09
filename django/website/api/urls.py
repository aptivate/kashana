from django.conf.urls import (
    include,
    url
)
from logframe.api import (
    router,
    SwitchLogframes
)

# URLs
urlpatterns = [
    url(r'^switch', SwitchLogframes.as_view(), name='switch-logframes'),
    url(r'^', include(router.urls)),
]
