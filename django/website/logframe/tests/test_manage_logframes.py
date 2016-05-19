from django.test.client import RequestFactory

from django_dynamic_fixture import N

from ..models import LogFrame
from ..views import ManageLogframes


def test_delete_column_not_displayed_if_only_one_logframe():
    view = ManageLogframes()
    view.table_data = [N(LogFrame)]
    view.request = RequestFactory().get('/')
    table = view.get_table()
    assert ('delete',) == table.exclude


def test_delete_column_displayed_if_more_than_one_logframe():
    view = ManageLogframes()
    view.table_data = [N(LogFrame), N(LogFrame)]
    view.request = RequestFactory().get('/')
    table = view.get_table()
    assert () == table.exclude
