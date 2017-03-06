# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_logframe_to_settings(apps, schema_editor):
    LogFrame = apps.get_model('logframe', 'LogFrame')
    Settings = apps.get_model('appconf', 'Settings')

    if not LogFrame.objects.exists():
        return

    first_logframe = LogFrame.objects.order_by('id')[0]
    remaining_logframes = LogFrame.objects.order_by('id')[1:]

    settings, _ = Settings.objects.get_or_create()
    settings.logframe = first_logframe
    settings.save()

    for logframe in remaining_logframes:
        # Clone the original settings for other logframes
        Settings.objects.create(
            logframe=logframe,
            max_result_level=settings.max_result_level,
            open_result_level=settings.open_result_level
        )


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0002_settings_logframe'),
    ]

    operations = [
        migrations.RunPython(add_logframe_to_settings)
    ]
