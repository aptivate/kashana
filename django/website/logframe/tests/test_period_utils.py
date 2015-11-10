from datetime import date, timedelta

from ..period_utils import get_month_shift, get_periods, periods_intersect


def test_get_month_shift_returns_next_period_start_date_within_same_year():
    new_month, add_year = get_month_shift(1, 12, 0)

    assert 1 == new_month
    assert 0 == add_year


def test_get_month_shift_returns_next_period_start_date_within_different_years():
    new_month, add_year = get_month_shift(11, 2, 1)

    assert 5 == new_month
    assert 1 == add_year


def test_get_month_shift_handles_december():
    new_month, _ = get_month_shift(12, 1)
    assert 12 == new_month


def test_get_periods_when_end_date_before_period_end():
    # This should produce eight periods, 2 for each of the years from
    # 2015 to 2018 inclusive
    periods = get_periods(date(2015, 01, 01), date(2018, 12, 31), 1, 2)
    assert 8 == len(periods)


def test_periods_instersect_for_no_second_period():
    s = date.today() - timedelta(days=1)
    e = date.today() + timedelta(days=1)
    assert periods_intersect(s, e, None, None)


def test_periods_intersect_for_when_second_start_date_less_than_first_end_date():
    s = date.today() - timedelta(days=1)
    e = date.today() + timedelta(days=1)
    x = date.today()

    assert periods_intersect(s, e, x, None)


def test_periods_intersect_for_when_second_end_date_greater_than_first_start_date():
    s = date.today() - timedelta(days=1)
    e = date.today() + timedelta(days=1)
    y = date.today()

    assert periods_intersect(s, e, None, y)


def test_periods_intersect_for_when_second_start_date_in_first_period():
    s = date.today() - timedelta(days=1)
    e = date.today() + timedelta(days=1)
    x = date.today()
    y = date.today()

    assert periods_intersect(s, e, x, y)


def test_periods_intersect_for_when_period_contains_first_period():
    s = date.today() - timedelta(days=1)
    e = date.today() + timedelta(days=1)
    x = date.today() - timedelta(days=2)
    y = date.today() + timedelta(days=2)

    assert periods_intersect(s, e, x, y)
