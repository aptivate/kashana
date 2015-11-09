from mock import Mock

from ..admin import RatingAdmin, SubIndicatorAdmin
from ..models import colors, Rating, SubIndicator


def test_sub_indicator_admin_rsult_returns_indicator_result():
    sub_indicator = Mock(indicator=Mock(result='result'))

    admin = SubIndicatorAdmin(SubIndicator, None)
    assert sub_indicator.indicator.result == admin.result(sub_indicator)


def test_rating_admin_colored_name_returns_name_for_colours():
    obj = Mock(color=colors[0][0])

    admin = RatingAdmin(Rating, None)
    assert '<span class="rating-list-item {0}">{1}</span>'.format(colors[0][0], colors[0][1]) == admin.colored_name(obj)
