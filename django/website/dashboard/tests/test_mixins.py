import pytest

from django_dynamic_fixture import G

from logframe.models import LogFrame

from ..mixins import OverviewMixin


@pytest.mark.django_db
def test_get_logframe_returns_new_logframe_if_none_exists():
    LogFrame.objects.all().delete()

    overview_mixin = OverviewMixin()
    log_frame = overview_mixin.get_logframe()

    assert log_frame == LogFrame.objects.get()


@pytest.mark.django_db
def test_get_logframe_returns_existing_logframe_where_one_exists():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame)

    overview_mixin = OverviewMixin()
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_returns_first_logframe_where_multiple_logframes_exist_by_default():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame
