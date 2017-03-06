# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_level_details(apps, schema_editor):
    ResultLevelName = apps.get_model('logframe', 'ResultLevelName')
    LogFrame = apps.get_model('logframe', 'LogFrame')
    for logframe in LogFrame.objects.all():
        ResultLevelName.objects.bulk_create([
            ResultLevelName(level_number=1, level_name="Goal", logframe=logframe),
            ResultLevelName(level_number=2, level_name="Outcome", logframe=logframe),
            ResultLevelName(level_number=3, level_name="Output", logframe=logframe),
            ResultLevelName(level_number=4, level_name="Activity", logframe=logframe)
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0006_resultlevelname'),
    ]

    operations = [
        migrations.RunPython(add_level_details)
    ]
