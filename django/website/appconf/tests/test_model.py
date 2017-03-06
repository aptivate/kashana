from appconf.models import Settings
from django_dynamic_fixture import N

from logframe.models import LogFrame


def test_settings_object_as_string_reads_settings():
    logframe = N(LogFrame)
    s = Settings(logframe=logframe)
    assert 'Settings for {0}'.format(logframe.name) == str(s)
