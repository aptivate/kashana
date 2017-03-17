# -*- coding: utf-8 -*-
from random import randint

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from django_dynamic_fixture import N, G
from mock import Mock, patch
from organizations.models import Organization
import pytest
from uuslug import uuslug

from appconf.models import Settings
from ..models import LogFrame
from ..views import CreateLogframe


def test_redirects_to_created_logframe_on_success():
    create_logframe_view = CreateLogframe()
    logframe = N(LogFrame, persist_dependencies=False)
    create_logframe_view.object = logframe
    assert reverse('logframe-dashboard', kwargs={'slug': logframe.slug, 'org_slug':logframe.organization.slug}) == create_logframe_view.get_success_url()


@pytest.mark.django_db
def test_instance_slug_set_when_creating_logframe():
    logframe = LogFrame(name='Test Name', slug='')
    logframe.organization = G(Organization)

    request = RequestFactory().post('/', {'name': 'Test Name'})
    create_logframe_view = CreateLogframe()
    create_logframe_view.request = request
    create_logframe_view.kwargs = {'org_slug': logframe.organization.slug}

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    # This must come before saving the logframe, otherwise the slug will be
    # different
    expected_slug_name = uuslug(logframe.name, logframe)

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
    create_logframe_view.kwargs = {'org_slug': logframe.organization.slug}

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    create_logframe_view.form_valid(form)
    logframe = LogFrame.objects.get(name='Test Name')
    try:
        Settings.objects.get(logframe=logframe)
    except Settings.DoesNotExist:
        pytest.fail("Settings should have been created for this logframe")


@pytest.mark.django_db
def test_logframe_created_with_organization():
    logframe = LogFrame(name='Test Name', slug='')
    organization = G(Organization)
    organization.slug = 'test'
    organization.save()

    request = RequestFactory().post('/', {'name': 'Test Name'})
    create_logframe_view = CreateLogframe()
    create_logframe_view.request = request
    create_logframe_view.kwargs = {'org_slug': 'test'}

    form_class = create_logframe_view.get_form_class()
    form = create_logframe_view.get_form(form_class)
    form.instance = logframe

    create_logframe_view.form_valid(form)
    logframe = LogFrame.objects.get(name='Test Name')
    assert logframe.organization.slug == 'test'
