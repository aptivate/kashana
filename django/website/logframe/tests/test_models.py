from __future__ import absolute_import, unicode_literals

from datetime import date
from collections import namedtuple
from unittest import TestCase
import pytest
from django_dynamic_fixture import G

from ..models import AverageTargetPercentMixin, LogFrame, Result, Period


class TestAverageTargetPercentMixin(TestCase):

    FakeChild = namedtuple('FakeChild', ['target_percent'])
    FakeWeightedChild = namedtuple('FakeWeightedChild', ['target_percent', 'impact_weighting'])

    def setUp(self):
        self.testobj = AverageTargetPercentMixin()

    def test_calculate_target_percent_returns_0_when_no_children(self):
        self.assertEqual(0, self.testobj._calculate_target_percent([]))

    def test_calculate_target_percent_returns_child_percent_when_one_child_present(self):
        child1 = self.FakeChild(43)
        self.assertEqual(43, self.testobj._calculate_target_percent([child1]))

    def test_calculate_target_percent_averages_two_children(self):
        child1 = self.FakeChild(45)
        child2 = self.FakeChild(55)
        self.assertEqual(50, self.testobj._calculate_target_percent([child1, child2]))

    def test_calculate_weighted_target_percent_returns_0_when_no_children(self):
        self.assertEqual(0, self.testobj._calculate_weighted_target_percent([]))

    def test_calculate_weighted_target_percent_returns_child_percent_when_one_child_present(self):
        child1 = self.FakeWeightedChild(43, 20)
        self.assertEqual(43, self.testobj._calculate_weighted_target_percent([child1]))

    def test_calculate_weighted_target_percent_averages_two_children(self):
        child1 = self.FakeWeightedChild(45, 20)
        child2 = self.FakeWeightedChild(60, 10)
        self.assertEqual(50, self.testobj._calculate_weighted_target_percent([child1, child2]))

    def test_calculate_summary_status_returns_ok_when_target_gt_budget(self):
        self.assertEqual(AverageTargetPercentMixin.OK,
                         self.testobj._calculate_summary_status(53, 52))

    def test_calculate_summary_status_returns_ok_when_target_equals_budget(self):
        self.assertEqual(AverageTargetPercentMixin.OK,
                         self.testobj._calculate_summary_status(52, 52))

    def test_calculate_summary_status_returns_warning_when_target_slightly_lt_budget(self):
        self.assertEqual(AverageTargetPercentMixin.WARNING,
                         self.testobj._calculate_summary_status(51, 52))

    def test_calculate_summary_status_returns_warning_when_target_10_lt_budget(self):
        self.assertEqual(AverageTargetPercentMixin.WARNING,
                         self.testobj._calculate_summary_status(42, 52))

    def test_calculate_summary_status_returns_danger_when_target_11_lt_budget(self):
        self.assertEqual(AverageTargetPercentMixin.DANGER,
                         self.testobj._calculate_summary_status(41, 52))


#
# Test Result
#
@pytest.mark.django_db
def test_get_absolute_url_returns_correct_path():
    from django.core.urlresolvers import reverse
    logframe = G(LogFrame)
    result = G(Result, log_frame=logframe)
    expected_url = reverse("design-result", args=[logframe.id, result.id])

    assert result.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_level_set_to_one_for_root_result():
    logframe = G(LogFrame)
    result = G(Result, log_frame=logframe, ignore_fields=['parent', 'level'])

    assert result.level == 1


@pytest.mark.django_db
def test_level_set_to_one_more_than_parent():
    logframe = G(LogFrame)
    result = G(Result, log_frame=logframe,
               ignore_fields=['parent', 'level'])
    result2 = G(Result, log_frame=logframe, parent=result,
                ignore_fields=['level'])

    assert result2.level == 2


@pytest.mark.django_db
def test_order_set_automatically_when_missing():
    logframe = G(LogFrame)
    result = G(Result, log_frame=logframe,
               ignore_fields=['parent', 'level', 'order'])
    assert result.order == 1

    result2 = G(Result, log_frame=logframe, parent=result, order=3,
                ignore_fields=['level', 'order'])
    assert result2.order == 1


@pytest.mark.django_db
def test_order_set_to_max_plus_one_of_siblings():
    logframe = G(LogFrame)
    G(Result, log_frame=logframe, order=1, level=2, ignore_fields=['parent'])
    G(Result, log_frame=logframe, order=2, level=2, ignore_fields=['parent'])
    G(Result, log_frame=logframe, order=3, level=1, ignore_fields=['parent'])
    result = G(Result, log_frame=logframe, level=2,
               ignore_fields=['parent', 'order'])
    assert result.order == 3


#
# Test Period
#
def test_get_period_returns_correct_periods():
    period = Period(log_frame_id=1, start_month=2, num_periods=4)
    start_date = date(2012, 6, 23)
    end_date = date(2014, 11, 11)

    periods = period.get_periods(start_date, end_date)
    expected = [
        {'start': date(2012, 5, 1),
         'name': 'May 2012'},
        {'start': date(2012, 8, 1),
         'name': 'August 2012'},
        {'start': date(2012, 11, 1),
         'name': 'November 2012'},
        {'start': date(2013, 2, 1),
         'name': 'February 2013'},
        {'start': date(2013, 5, 1),
         'name': 'May 2013'},
        {'start': date(2013, 8, 1),
         'name': 'August 2013'},
        {'start': date(2013, 11, 1),
         'name': 'November 2013'},
        {'start': date(2014, 2, 1),
         'name': 'February 2014'},
        {'start': date(2014, 5, 1),
         'name': 'May 2014'},
        {'start': date(2014, 8, 1),
         'name': 'August 2014'},
        {'start': date(2014, 11, 1),
         'name': 'November 2014'}
    ]
    assert periods == expected


def test_get_period_returns_correct_periods_also_for_start_of_the_year():
    period = Period(log_frame_id=1, start_month=2, num_periods=4)
    start_date = date(2013, 1, 1)
    end_date = date(2014, 11, 11)

    periods = period.get_periods(start_date, end_date)
    expected = [
        {'start': date(2012, 11, 1),
         'name': 'November 2012'},
        {'start': date(2013, 2, 1),
         'name': 'February 2013'},
        {'start': date(2013, 5, 1),
         'name': 'May 2013'},
        {'start': date(2013, 8, 1),
         'name': 'August 2013'},
        {'start': date(2013, 11, 1),
         'name': 'November 2013'},
        {'start': date(2014, 2, 1),
         'name': 'February 2014'},
        {'start': date(2014, 5, 1),
         'name': 'May 2014'},
        {'start': date(2014, 8, 1),
         'name': 'August 2014'},
        {'start': date(2014, 11, 1),
         'name': 'November 2014'}
    ]
    assert periods == expected


def test_get_period_returns_periods_interval():
    period = Period(log_frame_id=1, start_month=2, num_periods=4)
    p = period.get_period("2014-05-01")

    assert p == (date(2014, 5, 1), date(2014, 7, 31))


def test_get_period_correctly_crosses_end_of_year():
    period = Period(log_frame_id=1, start_month=1, num_periods=4)
    p = period.get_period("2014-11-01")

    assert p == (date(2014, 11, 1), date(2015, 1, 31))
