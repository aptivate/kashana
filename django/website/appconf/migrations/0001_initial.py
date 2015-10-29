# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_result_level', models.PositiveSmallIntegerField(default=4, help_text=b'Defines the depth of the result tree on MIS dashboard.', verbose_name=b'Result depth')),
                ('open_result_level', models.PositiveSmallIntegerField(default=2, help_text=b'Depth to which result elements are automatically expanded on MIS dashboard.', verbose_name=b'Expanded level')),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
