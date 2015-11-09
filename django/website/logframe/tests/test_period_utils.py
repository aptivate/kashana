from ..period_utils import get_month_shift


def test_get_month_shift_handles_december():
    new_month, _ = get_month_shift(12, 1)
    assert 12 == new_month
