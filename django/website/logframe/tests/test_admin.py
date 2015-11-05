from mock import Mock

from ..admin import SubIndicatorAdmin
from ..models import SubIndicator


def test_sub_indicator_admin_rsult_returns_indicator_result():
    sub_indicator = Mock(indicator=Mock(result='result'))

    admin = SubIndicatorAdmin(SubIndicator, None)
    assert sub_indicator.indicator.result == admin.result(sub_indicator)
