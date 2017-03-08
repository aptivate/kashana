# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('contacts', '0007_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameOnlyPermission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
    ]
