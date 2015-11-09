from datetime import date

from ..period_utils import get_month_shift, get_periods


def test_get_month_shift_handles_december():
    new_month, _ = get_month_shift(12, 1)
    assert 12 == new_month


def test_get_periods_when_end_date_before_period_end():
    # This should produce eight periods, 2 for each of the years from
    # 2015 to 2018 inclusive
    periods = get_periods(date(2015, 01, 01), date(2018, 12, 31), 1, 2)
    assert 8 == len(periods)
