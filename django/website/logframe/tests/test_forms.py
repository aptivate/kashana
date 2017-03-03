import pytest
from django_dynamic_fixture import G

from ..forms import CreateLogFrameForm
from ..models import LogFrame


@pytest.mark.django_db
def test_logframe_name_validation_error_message():
    G(LogFrame, name='test')
    form = CreateLogFrameForm(data={'name': 'test'})
    form.is_valid()

    assert ['A Logframe with this name already exists'] == form.errors['name']
