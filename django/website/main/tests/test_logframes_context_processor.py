from django_dynamic_fixture import N
from mock import Mock, patch

from logframe.models import LogFrame

from ..context_processors import logframe_list


@patch('logframe.models.LogFrame')
def test_logrames_context_processor_returns_list_of_logframes(logframe):
    logframes = N(LogFrame, n=3)
    logframe.objects = Mock(all=Mock(return_value=logframes))

    assert {'logframe_list': logframes} == logframe_list(None)
