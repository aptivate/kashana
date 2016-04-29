# -*- coding: utf-8 -*-
from random import randint
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

import pytest
from django_dynamic_fixture import N
from mock import Mock, patch

from ..models import LogFrame
from ..views import CreateLogframe


def test_redirects_to_created_logframe_on_success():
    create_logframe_view = CreateLogframe()
    logframe = N(LogFrame)
    create_logframe_view.object = logframe
    assert reverse('logframe-dashboard', kwargs={'slug': logframe.slug}) == create_logframe_view.get_success_url()


@patch('logframe.views.LogFrame')
def test_logframe_name_converted_to_lowercase(logframes):
    logframes.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = Mock()
    type(a_logframe).name = 'TesTCapSLowereD'

    create_logframe_view = CreateLogframe()
    expected_slug = 'testcapslowered'
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@patch('logframe.views.LogFrame')
def test_logframe_slug_only_contains_letters_numbers_hyphens_and_underscores(logframes):
    logframes.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = Mock()
    type(a_logframe).name = u'Test£$%^(-Name_Preserved'

    create_logframe_view = CreateLogframe()
    expected_slug = 'test-name_preserved'
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@patch('logframe.views.LogFrame')
def test_spaces_from_logframe_name_replaced_with_underscores(logframes):
    logframes.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = Mock()
    type(a_logframe).name = 'Test Name'

    create_logframe_view = CreateLogframe()
    expected_slug = 'test_name'
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@patch('logframe.views.LogFrame')
def test_unique_slug_never_longer_than_47_characters(logframes):
    logframes.objects.filter = Mock(return_value=Mock(exists=lambda: False))

    a_logframe = Mock()
    type(a_logframe).name = 'A Very Very Very Very Very Very Long Test Name Indeed'

    create_logframe_view = CreateLogframe()
    expected_slug = 'a_very_very_very_very_very_very_long_test_name'
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@patch('logframe.views.LogFrame')
def test_long_duplicate_slug_not_likely_to_go_over_fifty_characters(logframes):
    # The odds of ever actually having 998 logframes with a similar slug is
    # small enough that it makes a good maximum value to keep within the 50
    # character limit
    count = 998
    logframes.objects.filter = Mock(
        return_value=Mock(exists=lambda: True, count=lambda: count)
    )

    a_logframe = Mock()
    type(a_logframe).name = 'A Very Very Very Very Very Very Long Test Name Indeed'

    create_logframe_view = CreateLogframe()
    expected_slug = 'a_very_very_very_very_very_very_long_test_name999'
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@patch('logframe.views.LogFrame')
def test_slug_for_logframe_always_unique(logframes):
    count = randint(1, 10)
    logframes.objects.filter = Mock(
        return_value=Mock(exists=lambda: True, count=lambda: count)
    )

    a_logframe = Mock()
    type(a_logframe).name = 'Duplicate Name'

    create_logframe_view = CreateLogframe()
    expected_slug = 'duplicate_name' + unicode(count + 1)
    actual_slug = create_logframe_view.get_unique_slug_name(a_logframe)

    assert expected_slug == actual_slug


@pytest.mark.django_db
def test_instance_slug_set_when_creating_logframe():
    logframe = LogFrame(name='Test Name', slug='')

    request = RequestFactory().post('/', {'name': 'Test Name'})
    create_logframe_view = CreateLogframe()
    create_logframe_view.request = request

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    # This must come before saving the logframe, otherwise the slug will be
    # different
    expected_slug_name = create_logframe_view.get_unique_slug_name(logframe)

    create_logframe_view.form_valid(form)
    logframe = LogFrame.objects.get(name='Test Name')

    assert expected_slug_name == logframe.slug
