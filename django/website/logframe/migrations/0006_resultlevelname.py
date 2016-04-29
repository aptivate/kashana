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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_number', models.IntegerField()),
                ('level_name', models.CharField(max_length=128)),
                ('logframe', models.ForeignKey(to='logframe.LogFrame')),
            ],
        ),
    ]
