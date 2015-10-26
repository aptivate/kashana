from __future__ import unicode_literals, absolute_import

import datetime
import pytest
import mock

from django_dynamic_fixture import G
from django.core.urlresolvers import reverse
from django.test import TestCase

from contacts.tests.factories import UserFactory
from logframe.models import (
    Activity,
    Indicator,
    LogFrame,
    Period,
    Result
)

from ..views import (
    ExportPlanMixin,
    gant_fill,
    ExportAnnualPlan,
    ExportIndicator,
    LogframeDataMixin
)


class TestExportViews(TestCase):

    def setUp(self):
        self.log_frame = G(LogFrame)
        self.period = G(Period, log_frame=self.log_frame, start_month=7,
                        num_periods=4)
        self.result = G(Result, log_frame=self.log_frame, ignore_fields=['parent', 'rating'])

        # Create other indicator to prove logframe filtering works.
        other_logframe = G(LogFrame, name='Test Log Frame 1')
        assert self.log_frame != other_logframe
        other_result = G(Result, log_frame=other_logframe, ignore_fields=['parent', 'rating'])
        G(Indicator, result=other_result)

    def add_result(self, name, parent=None):
        return G(Result, log_frame=self.log_frame,
                 name=name, parent=parent,
                 ignore_fields=['level', 'order', 'rating'])

    def add_desendents(self, parent, names):
        results = []
        for i, name in enumerate(names):
            result = self.add_result(name, parent)
            parent = result
            results.append(result)
        return results

    def test_export_indicator_renders_indicator_in_logframe(self):
        export_indicator = ExportIndicator(self.log_frame)
        indicator = G(Indicator, result=self.result)

        self.assertEqual([
            indicator.name,
            indicator.description],
            export_indicator.render(indicator))

        indicator = G(Indicator, result=G(Result, log_frame=G(LogFrame, name='Test Log Frame 2'), ignore_fields=['parent', 'rating']))

        self.assertNotEqual(indicator.result.log_frame, self.log_frame)

        self.assertEqual([
            indicator.name,
            indicator.description],
            export_indicator.render(indicator))

    def test_flattern_result_object_hierarchy(self):
        """
            Impact ->
            Outcome ->

            Output 1 ->
                Result 1.1 ->
                    Result 1.1.1 ->
                        Result 1.1.1.1

            ...

            Gives a flat list in hiearchy order.
        """
        impact = self.add_result("Impact")  # top of hierarchy
        outcome = self.add_result("Outcome", impact)

        output_1 = ["Output 1", "Result 1.1", "Result 1.1.1", "Result 1.1.1.1"]
        output_2 = ["Output 2", "Result 2.2", "Result 2.2.2", "Result 2.2.2.2"]

        results_1 = self.add_desendents(outcome, output_1)
        results_2 = self.add_desendents(outcome, output_2)

        # assert output 1 and 2 have the same levels
        # they should also be increasing (untested)
        self.assertEqual([o.level for o in results_1],
                         [o.level for o in results_2])

        logframe_data = LogframeDataMixin()
        logframe_data.period = self.period
        actual_results = logframe_data.get_results(self.log_frame)

        expected_results = [impact, outcome] + results_1 + results_2
        self.assertEqual(expected_results, actual_results)

    def test_resolve_activities_for_last_results(self):
        """ Given a list of results, for results which are leaf nodes add
        activities (if any exist) """
        top = self.add_result("Top")
        names = ["Result 1", "Result 1.1"]
        results = self.add_desendents(top, names)
        all_results = [top] + results

        last_result = results[-1]
        activity = G(Activity, log_frame=self.log_frame, result=last_result)

        logframe_data = LogframeDataMixin()
        logframe_data.period = self.period
        logframe_data.year = 2014
        logframe_data.logframe = self.log_frame
        results_with_activities = list(logframe_data.add_activities(all_results))

        expected_results = [
            (top, None),
            (results[0], None),
            (results[1], [activity]),
        ]

        self.assertEqual(expected_results, results_with_activities)

    def test_activities_ordered_by_start_date(self):
        """ Expect the earliest starting activities to appear first (Gantt
        chart like) """
        top = self.add_result("Top")

        activities = []
        # add in reversed order to attempt to proove we're not just asserting
        # results returned in DB insertion order are true.
        for i in reversed(range(5)):
            start_date = datetime.date(2014, 7, i + 1)
            end_date = start_date + datetime.timedelta(days=1)

            activities.append(
                G(Activity, log_frame=self.log_frame,
                  result=top,
                  start_date=start_date,
                  end_date=end_date
                  )
            )

        # Expect unorderable activities to appear first
        unordered_activity = G(Activity, log_frame=self.log_frame, result=top,
                               start_date=None)

        logframe_data = LogframeDataMixin()
        logframe_data.logframe = self.log_frame
        logframe_data.period = self.period
        logframe_data.year = 2014

        results_with_activities = list(
            logframe_data.add_activities([top]))

        expected_activities = [unordered_activity] + list(reversed(activities))
        actual_activities = results_with_activities[0][1]

        start_dates = lambda xs: [x.start_date for x in xs]
        self.assertEqual(start_dates(actual_activities), start_dates(expected_activities))

    def test_rendering_hierarchy(self):
        # levels have different render methods
        pass

    def test_filtering_objects_in_annual_period(self):
        """ Activities should appear on an annual plan are if their calendar
        dates fall within the project period for the logframe (see the Period model).
        """
        result = self.add_result("Result")

        def add_activity(start, end):
            return G(
                Activity,
                log_frame=self.log_frame,
                result=result,
                start_date=datetime.date(*start),
                end_date=datetime.date(*end),
            )

        # Test cases for the 2014 planning year (2014/7 to 2015/7)

        not_expected = [
            ((2012, 1, 1), (2013, 1, 1)),  # before 2014, don't expect
            ((2014, 1, 1), (2014, 6, 1)),  # before 2014 planning, don't expect
            ((2015, 7, 1), (2015, 11, 1)),  # after 2014 planning, don't expect
        ]

        for start, end in not_expected:
            add_activity(start, end)

        expected = [
            ((2013, 6, 1), (2015, 7, 1)),  # crosses all periods
            ((2014, 6, 1), (2014, 8, 1)),  # crosses first period
            ((2014, 7, 1), (2014, 8, 1)),  # exists in period
            ((2014, 7, 1), (2015, 6, 1)),  # exists in period
            ((2015, 6, 1), (2015, 7, 1)),  # crosses last period
        ]

        expected_activities = []
        for start, end in expected:
            expected_activities.append(add_activity(start, end))

        logframe_data = LogframeDataMixin()
        logframe_data.logframe = self.log_frame
        logframe_data.period = self.period
        logframe_data.year = 2014  # Expect this to be set by the view
        actual_activities = logframe_data.get_activities(result)

        ids = lambda xs: [x.id for x in xs]
        self.assertEqual(ids(expected_activities),
                         ids(actual_activities))

    def test_invalid_date_range_treated_as_undated(self):
        result = self.add_result("Result")
        activity = G(Activity, log_frame=self.log_frame,
                     result=result,
                     start_date=datetime.date(2015, 1, 1),
                     end_date=datetime.date(2013, 1, 1))

        logframe_data = LogframeDataMixin()
        logframe_data.period = self.period
        logframe_data.logframe = self.log_frame
        logframe_data.year = 2014  # Expect this to be set by the view

        # Expect the activity with invalid range to be included
        ids = lambda xs: [x.id for x in xs]
        self.assertEqual(ids([activity]),
                         ids(logframe_data.get_activities(result)))

    @pytest.mark.integration
    def test_annual_plan_get_data(self):
        impact = self.add_result("Impact")  # top of hierarchy
        outcome = self.add_result("Outcome", impact)

        output_1 = ["Output 1", "Result 1.1"]
        results_1 = self.add_desendents(outcome, output_1)
        last_result = results_1[-1]
        last_result.description = "Result description"
        last_result.save()

        activities = []
        for i in range(3):
            activities.append(
                G(Activity, log_frame=self.log_frame, result=last_result))

        view = ExportAnnualPlan()
        view.logframe = self.log_frame
        view.period = self.period
        view.kwargs = {'pk': self.log_frame.pk}
        view.year = 2014
        view.start_date = datetime.date(2014, self.period.start_month, 1)
        data = view.get_data()

        self.assertEqual('2014 Annual Report', data[0][0])

    @pytest.mark.integration
    @pytest.mark.client
    def test_export_annual_plan(self):
        # Can we log in?
        user = UserFactory()
        user.set_password("test")
        user.save()

        self.client.login(username=user.business_email, password="test")

        response = self.client.get(
            reverse(
                'export-annual-plan',
                kwargs={
                    'pk': self.log_frame.pk,
                    'year': '2014',
                }
            )
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="%s"' % '2014_annual_plan.xlsx')


class TestExportPlanMixin(TestCase):
    def test_get_period_header(self):
        start = datetime.date(2014, 1, 1)
        months = ExportPlanMixin.get_period_header(start, padding=0)
        expected = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec']
        self.assertEqual(expected, months)

        start = datetime.date(2014, 4, 1)
        months = ExportPlanMixin.get_period_header(start, padding=0)
        expected = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
                    'Dec', 'Jan', 'Feb', 'Mar']
        self.assertEqual(expected, months)

    def test_get_period_header_with_padding(self):
        start = datetime.date(2014, 1, 1)
        months = ExportPlanMixin.get_period_header(start, padding=3)
        expected = ['', '', '', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.assertEqual(expected, months)

    def test_get_period_header_with_end_date(self):
        start = datetime.date(2014, 4, 1)
        end = datetime.date(2014, 6, 30)
        months = ExportPlanMixin.get_period_header(start, end, padding=1)
        expected = ['', 'Apr', 'May', 'Jun']
        self.assertEqual(expected, months)

        start = datetime.date(2014, 10, 1)
        end = datetime.date(2015, 2, 1)
        months = ExportPlanMixin.get_period_header(start, end, padding=1)
        expected = ['', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        self.assertEqual(expected, months)

        start = datetime.date(2014, 8, 1)
        end = datetime.date(2015, 3, 1)
        months = ExportPlanMixin.get_period_header(start, end, padding=0)
        expected = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        self.assertEqual(expected, months)

    def test_get_period_list(self):
        periods = ExportPlanMixin.get_period_list(datetime.date(2014, 5, 1),
                                                  datetime.date(2014, 8, 11))
        expected = [
            (datetime.date(2014, 5, 1), datetime.date(2014, 5, 31)),
            (datetime.date(2014, 6, 1), datetime.date(2014, 6, 30)),
            (datetime.date(2014, 7, 1), datetime.date(2014, 7, 31)),
            (datetime.date(2014, 8, 1), datetime.date(2014, 8, 31)),
        ]
        self.assertEqual(expected, periods)

    def test_mark_row(self):
        mark = {
            'value': "",
            'styles': {'fill': gant_fill}
        }
        start = datetime.date(2014, 8, 1)
        end = datetime.date(2014, 9, 30)
        periods = [
            (datetime.date(2014, 7, 1), datetime.date(2014, 7, 31)),
            (datetime.date(2014, 8, 1), datetime.date(2014, 8, 31)),
            (datetime.date(2014, 9, 1), datetime.date(2014, 9, 30)),
            (datetime.date(2014, 10, 1), datetime.date(2014, 10, 31)),
        ]

        # Without padding
        marked = ExportPlanMixin.mark_row(start, end, periods, padding=0)
        expected = ["", mark, mark, ""]
        self.assertEqual(expected, marked)

        # With padding
        marked = ExportPlanMixin.mark_row(start, end, periods, padding=2)
        expected = ["", "", "", mark, mark, ""]
        self.assertEqual(expected, marked)

    def test_add_row(self):
        view = ExportPlanMixin()

        view.data = []
        row = [1, 2, 3, 4, 5]
        padding = ["", "", ""]
        expected = padding + row
        view.add_row(row, len(padding))
        self.assertEqual([expected], view.data)

        view.data = []
        row = [1, 2, 3, 4, 5]
        padding = ["", "", "", "", ""]
        expected = padding + row
        view.add_row(row, len(padding))
        self.assertEqual([expected], view.data)

    # get_data tested by test_annual_plan_get_data
