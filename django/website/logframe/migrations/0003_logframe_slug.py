# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0002_auto_20151215_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='logframe',
            name='slug',
            field=models.SlugField(unique=True, null=True),
        ),
    ]
