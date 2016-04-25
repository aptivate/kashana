# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0005_auto_20151215_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultLevelName',
            fields=[
                ('level_number', models.IntegerField(serialize=False, primary_key=True)),
                ('level_name', models.CharField(max_length=128)),
            ],
        ),
    ]
