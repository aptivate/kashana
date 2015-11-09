from appconf.models import Settings


def test_settings_object_as_string_reads_settings():
    s = Settings()
    assert 'Settings' == str(s)
