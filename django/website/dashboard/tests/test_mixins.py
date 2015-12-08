import pytest

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

    expected_log_frame = LogFrame.objects.create()

    overview_mixin = OverviewMixin()
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame
