import pytest
import mock

from datetime import date
from django_dynamic_fixture import G
from django.contrib.auth.models import Permission
from contacts.group_permissions import GroupPermissions
from ..mixins import AptivateDataBaseMixin, QuerysetSerializer
from ..models import LogFrame, Result, Period, Milestone
from contacts.models import User
from appconf.models import Settings


def test_queryserializer_creates_correct_serializer():
    s = Settings()
    serializer = QuerysetSerializer.create_serializer(Settings)
    data = serializer(s).data
    fields = s._meta.fields

    assert isinstance(data, dict) is True
    for field in fields:
        if field.name != "id" and field.default:
            assert data[field.name] == field.default


@pytest.mark.django_db
def test_json_object_list_serializes_correctly_given_model():
    s = Settings.objects.create()
    data = {}
    for field in s._meta.fields:
        data[field.name] = getattr(s, field.name)

    serialized = QuerysetSerializer._json_object_list(Settings.objects.all(),
                                                      None,
                                                      Settings)
    assert serialized == [data]


@pytest.mark.django_db
def test_get_logframe_data_contains_logframe():
    lf = G(LogFrame)
    mixin = AptivateDataBaseMixin()
    data = mixin.get_logframe_data(lf)

    assert 'logframe' in data
    assert data['logframe']['id'] == lf.id


@pytest.mark.django_db
def test_get_logframe_data_contains_results():
    lf = G(LogFrame)
    r = G(Result, log_frame=lf)
    r2 = G(Result, log_frame=lf)
    mixin = AptivateDataBaseMixin()
    data = mixin.get_logframe_data(lf)
    result_ids = set([r.id, r2.id])

    assert 'results' in data
    assert set([r["id"] for r in data['results']]) == result_ids


@pytest.mark.django_db
def test_get_logframe_data_contains_users():
    lf = G(LogFrame)
    u1 = G(User)
    u2 = G(User)
    mixin = AptivateDataBaseMixin()
    data = mixin.get_logframe_data(lf)
    user_ids = set([u1.id, u2.id])

    assert 'users' in data
    assert set([u["id"] for u in data['users']]) == user_ids


@pytest.mark.django_db
def test_get_logframe_data_contains_conf():
    s = Settings()
    fields = s._meta.fields
    lf = G(LogFrame)
    Settings.objects.create()

    mixin = AptivateDataBaseMixin()
    data = mixin.get_logframe_data(lf)
    assert 'conf' in data
    assert 'id' not in data['conf']
    for field in fields:
        if field.name != "id" and field.default:
            assert data['conf'][field.name] == field.default


@pytest.mark.django_db
def test_is_editable_fails_on_non_editors():
    u1 = G(User)
    mixin = AptivateDataBaseMixin()
    mixin.request = mock.Mock()
    mixin.request.user = u1
    assert mixin.is_editable() is False


@pytest.mark.django_db
def test_is_editable_succeeds_on_editors():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    edit_perm = Permission.objects.get(codename='edit_logframe')
    u1 = G(User)
    u1.user_permissions.add(edit_perm)

    mixin = AptivateDataBaseMixin()
    mixin.request = mock.Mock()
    mixin.request.user = u1
    assert mixin.is_editable() is True


@pytest.mark.django_db
def test_get_periods_creates_period_if_it_does_not_exist():
    assert Period.objects.exists() is False

    lf = G(LogFrame)
    mixin = AptivateDataBaseMixin()
    periods = mixin.get_periods(lf)

    assert Period.objects.exists() is True
    p = Period.objects.get()
    assert p.log_frame == lf
    assert periods == []


@pytest.mark.django_db
def test_get_periods_returns_correct_periods():
    lf = G(LogFrame)
    G(Milestone, log_frame=lf, date=date(2013, 8, 1))
    G(Milestone, log_frame=lf, date=date(2014, 1, 1))

    mixin = AptivateDataBaseMixin()
    periods = mixin.get_periods(lf)
    expected = [
        {'name': 'July 2013',
         'start': date(2013, 7, 1)},
        {'name': 'October 2013',
         'start': date(2013, 10, 1)},
        {'name': 'January 2014',
         'start': date(2014, 1, 1)},
    ]

    assert periods == expected
