import pytest
from django_dynamic_fixture import G

from ..forms import CreateLogFrameForm
from ..models import LogFrame


@pytest.mark.django_db
def test_logframe_with_duplication_name_raises_validation_error_message():
    G(LogFrame, name='test')
    form = CreateLogFrameForm(data={'name': 'test'})
    form.is_valid()

    assert ['A Logframe with this name already exists'] == form.errors['name']


@pytest.mark.django_db
def test_logframe_name_with_only_spaces_raises_validation_error_message():
    form = CreateLogFrameForm(data={'name': ' '})
    form.is_valid()

    assert ['The Logframe name must contain non-whitespace characters'] == form.errors['name']


@pytest.mark.django_db
def test_logframe_name_with_only_tabs_raises_validation_error_message():
    form = CreateLogFrameForm(data={'name': '\t'})
    form.is_valid()

    assert ['The Logframe name must contain non-whitespace characters'] == form.errors['name']
