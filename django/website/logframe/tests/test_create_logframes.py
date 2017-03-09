# -*- coding: utf-8 -*-
from random import randint

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from django_dynamic_fixture import N, G
from mock import Mock, patch
from organizations.models import Organization
import pytest

from appconf.models import Settings
from ..models import LogFrame
from ..views import CreateLogframe


def test_redirects_to_created_logframe_on_success():
    create_logframe_view = CreateLogframe()
    logframe = N(LogFrame, persist_dependencies=False)
    create_logframe_view.object = logframe
    assert reverse('logframe-dashboard', kwargs={'slug': logframe.slug, 'org_slug':logframe.organization.slug}) == create_logframe_view.get_success_url()


def test_logframe_name_converted_to_lowercase():
    temp_filter = LogFrame.objects.filter
    LogFrame.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = LogFrame()
    a_logframe.name = 'TesTCapSLowereD'

    expected_slug = 'testcapslowered'
    actual_slug = a_logframe.get_unique_slug_name()
    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


def test_logframe_slug_only_contains_letters_numbers_hyphens_and_underscores():
    temp_filter = LogFrame.objects.filter
    LogFrame.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = LogFrame()
    a_logframe.name = u'Test£$%^(-Name_Preserved'

    expected_slug = 'test-name_preserved'
    actual_slug = a_logframe.get_unique_slug_name()
    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


def test_spaces_from_logframe_name_replaced_with_underscores():
    temp_filter = LogFrame.objects.filter
    LogFrame.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = LogFrame()
    a_logframe.name = 'Test Name'

    expected_slug = 'test-name'
    actual_slug = a_logframe.get_unique_slug_name()
    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


def test_unique_slug_never_longer_than_50_characters():
    temp_filter = LogFrame.objects.filter
    LogFrame.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = LogFrame()
    a_logframe.name = 'A Very Very Very Very Very Very Long Test Name Indeed'

    expected_slug = 'a-very-very-very-very-very-very-long-test-name-ind'
    actual_slug = a_logframe.get_unique_slug_name()
    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


def test_long_duplicate_slug_not_likely_to_go_over_fifty_characters():
    # The odds of ever actually having 998 logframes with a similar slug is
    # small enough that it makes a good maximum value to keep within the 50
    # character limit
    count = 998
    temp_filter = LogFrame.objects.filter
    LogFrame.objects.filter = Mock(
        return_value=Mock(exists=Mock(side_effect=[True, False]), count=lambda: count)
    )

    a_logframe = LogFrame()
    a_logframe.name = 'A Very Very Very Very Very Very Long Test Name Indeed'

    expected_slug = 'a-very-very-very-very-very-very-long-test-name-999'

    actual_slug = a_logframe.get_unique_slug_name()
    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


def test_slug_for_logframe_always_unique():
    count = randint(1, 10)
    temp_filter = LogFrame.objects.filter

    LogFrame.objects.filter = Mock(
        return_value=Mock(exists=Mock(side_effect=[True, False]), count=lambda: count)
    )

    a_logframe = LogFrame()
    a_logframe.name = 'Duplicate Name'

    expected_slug = 'duplicate-name' + unicode(count + 1)
    actual_slug = a_logframe.get_unique_slug_name()

    LogFrame.objects.filter = temp_filter

    assert expected_slug == actual_slug


@pytest.mark.django_db
def test_instance_slug_set_when_creating_logframe():
    logframe = LogFrame(name='Test Name', slug='')
    logframe.organization = G(Organization)

    request = RequestFactory().post('/', {'name': 'Test Name'})
    create_logframe_view = CreateLogframe()
    create_logframe_view.request = request

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    # This must come before saving the logframe, otherwise the slug will be
    # different
    expected_slug_name = logframe.get_unique_slug_name()

    create_logframe_view.form_valid(form)
    logframe = LogFrame.objects.get(name='Test Name')

    assert expected_slug_name == logframe.slug


@pytest.mark.django_db
def test_settings_created_along_with_logframe():
    logframe = LogFrame(name='Test Name', slug='')
    logframe.organization = G(Organization)

    request = RequestFactory().post('/', {'name': 'Test Name'})
    create_logframe_view = CreateLogframe()
    create_logframe_view.request = request

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    create_logframe_view.form_valid(form)
    logframe = LogFrame.objects.get(name='Test Name')
    try:
        Settings.objects.get(logframe=logframe)
    except Settings.DoesNotExist:
        pytest.fail("Settings should have been created for this logframe")

