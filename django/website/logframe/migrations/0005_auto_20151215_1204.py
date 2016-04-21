# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0004_auto_20151215_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logframe',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
