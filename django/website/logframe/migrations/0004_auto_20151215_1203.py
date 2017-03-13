# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import migrations

from uuslug import uuslug


def set_logframe_slug(apps, schema_editor):
    LogFrame = apps.get_model('logframe', 'LogFrame')
    for logframe in LogFrame.objects.all():
        logframe.slug = uuslug(logframe.name, logframe)
        logframe.save()


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0003_logframe_slug'),
    ]

    operations = [
        migrations.RunPython(set_logframe_slug)
    ]
