# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_default_logframe(apps, schema_editor):
    LogFrame = apps.get_model('logframe', 'LogFrame')
    Organization = apps.get_model('organizations', 'Organization')
    if LogFrame.objects.exists():
        default_org = Organization.objects.create(name='Default Org')
        for logframe in LogFrame.objects.all():
            logframe.organization = default_org
            logframe.save()


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0010_logframe_organization'),
    ]

    operations = [
        migrations.RunPython(create_default_logframe)
    ]
