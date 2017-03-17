from django_dynamic_fixture import N
from mock import Mock, patch

from logframe.models import LogFrame

from ..context_processors import logframe_list
from django.test.client import RequestFactory


@patch('logframe.models.LogFrame')
def test_logrames_context_processor_returns_list_of_logframes(logframe):
    logframes = N(LogFrame, n=3, persist_dependencies=False)
    logframe.objects = Mock(filter=Mock(return_value=logframes))

    request = RequestFactory().get('/')
    request.user = Mock()

    assert {'logframe_list': logframes} == logframe_list(request)
