from django.core.urlresolvers import reverse

import pytest
from django_dynamic_fixture import N

from ..models import LogFrame
from ..views import CreateLogframe


def test_redirects_to_created_logframe_on_success():
    create_logframe_view = CreateLogframe()
    logframe = N(LogFrame)
    create_logframe_view.object = logframe
    assert reverse('logframe-dashboard', kwargs={'slug': logframe.slug}) == create_logframe_view.get_success_url()
