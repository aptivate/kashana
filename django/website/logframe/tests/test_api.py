from datetime import date, timedelta
from inspect import isfunction

from django.contrib.auth.models import Permission
from django.db.models.query_utils import Q
from django.test.client import RequestFactory

from django_dynamic_fixture import G
import mock
import pytest
from rest_framework.request import Request

from contacts.models import User
from contacts.group_permissions import GroupPermissions
from ..api import (
    CanEditOrReadOnly,
    ColumnViewSet,
    FilterRelationship,
    IDFilterBackend,
    PeriodOverlapFilterBackend,
    get_period_filter
)


@pytest.mark.django_db
def test_default_user_can_read_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)

    request = mock.Mock(method="GET", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is True


@pytest.mark.django_db
def test_default_user_can_not_change_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)

    request = mock.Mock(method="POST", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is False


@pytest.mark.django_db
def test_editor_can_change_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)
    edit_perm = Permission.objects.get(codename='edit_logframe')
    u1.user_permissions.add(edit_perm)

    request = mock.Mock(method="POST", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is True


def test_id_filter_backend_filter_queryset_filters_on_ids():
    request = RequestFactory().get('/?id=1&id=2&id=3')
    request = Request(request)
    id_filter_backend = IDFilterBackend()
    mock_queryset = mock.Mock(filter=mock.Mock())
    id_filter_backend.filter_queryset(request, mock_queryset, None)

    mock_queryset.filter.assert_called_with(id__in=[1, 2, 3])


def test_get_period_filter_returns_function():
    start_date = date.today() - timedelta(days=1)
    end_date = date.today()
    ret_val = get_period_filter(start_date, end_date, 'start_date', 'end_date')
    assert isfunction(ret_val)


def test_get_period_filter_function_filters_queryset():
    start_date = date.today() - timedelta(days=1)
    end_date = date.today()

    rel_1 = Q(**{'start_date__gte': start_date}) & Q(**{'start_date__lte': end_date})
    rel_2 = Q(**{'start_date__lte': start_date}) & Q(**{'end_date__gte': start_date})
    rel_3 = Q(**{'start_date__lte': end_date}) & Q(**{'end_date': None})
    rel_4 = Q(**{'end_date__gte': start_date}) & Q(**{'start_date': None})
    rel_5 = Q(**{'start_date': None}) & Q(**{'end_date': None})

    expected_query = rel_1 | rel_2 | rel_3 | rel_4 | rel_5

    mock_queryset = mock.Mock(filter=mock.Mock())
    filter_func = get_period_filter(start_date, end_date, 'start_date', 'end_date')
    filter_func(mock_queryset)

    actual_query = mock_queryset.filter.call_args[0][0]

    assert unicode(expected_query) == unicode(actual_query)


@mock.patch('logframe.api.get_period_filter')
def test_period_overlap_filter_backend_filter_queryset_filters_queryset(get_period_filter_func):
    request = RequestFactory().get('/?start_date=20151105&end_date=20151104')
    request = Request(request)

    get_period_filter_func.return_value = mock.Mock()

    mock_queryset = mock.Mock(filter=mock.Mock())

    filter_backend = PeriodOverlapFilterBackend()
    filter_backend.filter_queryset(
        request,
        mock_queryset,
        mock.Mock(lookup_period_start='start_date', lookup_period_end='end_date')
    )

    get_period_filter_func.assert_called_with('20151105', '20151104', 'start_date', 'end_date')
    get_period_filter_func.return_value.assert_called_with(mock_queryset)


def test_filter_relationship_backend_queryset_filters_on_relationship():
    filter_relationship = FilterRelationship()
    filter_relationship.lookup_rel = 'foreign_key_id'
    filter_relationship.kwargs = {'logframe_pk': '1'}
    filter_relationship.model = mock.Mock(objects=mock.Mock(filter=mock.Mock()))

    filter_relationship.get_queryset()

    filter_relationship.model.objects.filter.assert_called_with(**{'foreign_key_id': '1'})


def test_column_view_set_get_queryset_orders_by_date_and_id():
    column_view_set = ColumnViewSet()
    column_view_set.kwargs = {'logframe_pk': '1'}

    queryset = column_view_set.get_queryset()

    assert ['date', 'id'] == queryset.query.order_by
