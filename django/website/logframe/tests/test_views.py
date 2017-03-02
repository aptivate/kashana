import pytest
import json

from unittest import TestCase
from django_dynamic_fixture import G, N
from organizations.models import Organization

from ..views import ResultEditor, ResultMonitor
from ..models import (
    LogFrame,
    Result,
    Assumption,
    Rating,
)
from ..api import ResultSerializer


class ResultEditorTests(TestCase):
    def setUp(self):
        self.view = ResultEditor()
        logframe = G(LogFrame, id=25, name="Logframe")
        rating = G(Rating, log_frame=logframe)
        result = G(Result, log_frame=logframe, rating=rating, ignore_fields=['parent'])
        self.view.object = result

    @pytest.mark.django_db
    def test_data_in_context(self):
        context = self.view.get_context_data()
        data = self.view.get_data(self.view.object.log_frame, {})
        self.assertTrue('data' in context)

        data_dict = json.loads(context['data'])
        for item in data:
            assert item in data_dict
            assert data_dict[item] == data[item]

    @pytest.mark.django_db
    def test__json_object_list(self):
        lf = G(LogFrame)
        G(Result, name="Impact", log_frame=lf, ignore_fields=['parent', 'rating'])
        G(Result, name="Outcome", log_frame=lf, ignore_fields=['parent', 'rating'])
        results = self.view._json_object_list(lf.results, ResultSerializer)
        self.assertEqual(len(results), 2)
        results_names = set([r['name'] for r in results])
        self.assertEqual(set(["Impact", "Outcome"]), results_names)

    @pytest.mark.django_db
    def test_get_data_has_assumptions(self):
        lf = self.view.object.log_frame
        r1 = G(Result, name="Outcome", log_frame=lf, ignore_fields=['parent', 'rating'])
        self.view.object = r1
        G(Assumption, description='one', result=r1)
        G(Assumption, description='two', result=r1)
        r2 = G(Result, name="Output", log_frame=lf, ignore_fields=['parent', 'rating'])
        G(Assumption, description='three', result=r2)
        G(Assumption, description='four', result=G(Result, log_frame=G(LogFrame, name='Logframe 2'), ignore_fields=['parent', 'rating']))

        full_dict = self.view.get_data(lf, {})

        self.assertTrue('assumptions' in full_dict)
        results = full_dict['assumptions']
        self.assertEqual(3, len(results))


class ResultMonitorTests(TestCase):
    @pytest.mark.django_db
    def test_result_monitor_get_logframe_returns_result_logframe(self):
        organization = Organization.objects.create(name='Test Org')
        log_frame, _ = LogFrame.objects.get_or_create(name='Test Logframe', organization=organization)

        result = Result(log_frame=log_frame)
        result_monitor_view = ResultMonitor()
        result_monitor_view.object = result

        assert log_frame == result_monitor_view.get_logframe()

    def test_result_monitor_get_data_contains_serialised_result(self):
        log_frame = N(LogFrame, id=1, persist_dependencies=False)

        result = N(Result, ignore_fields=['log_frame', 'parent', 'rating', 'risk_rating'])
        result.log_frame = log_frame

        result_monitor_view = ResultMonitor()
        result_monitor_view.object = result

        expected_data = {
            'id': result.id,
            'name': result.name,
            'description': result.description,
            'order': result.order,
            'parent': None,
            'level': result.level,
            'contribution_weighting': result.contribution_weighting,
            'risk_rating': None,
            'rating': None,
            'log_frame': log_frame.id,
            'indicators': [],
            'activities': [],
            'assumptions': []
        }

        actual_data = result_monitor_view.get_data(log_frame, {})

        assert expected_data == actual_data['result']

