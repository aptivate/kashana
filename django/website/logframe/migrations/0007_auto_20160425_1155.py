# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_level_details(apps, schema_editor):
    ResultLevelName = apps.get_model('logframe', 'ResultLevelName')
    ResultLevelName.objects.bulk_create([
        ResultLevelName(level_number=1, level_name="Goal"),
        ResultLevelName(level_number=2, level_name="Output"),
        ResultLevelName(level_number=3, level_name="Outcome"),
        ResultLevelName(level_number=4, level_name="Activity")
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0006_resultlevelname'),
    ]

    operations = [
        migrations.RunPython(add_level_details)
    ]
