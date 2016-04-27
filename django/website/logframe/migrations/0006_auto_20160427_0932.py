# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0005_auto_20151215_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logframe',
            name='slug',
            field=models.SlugField(help_text="A 'slug' can consist of letters, numbers, underscores or hyphens and can be up to 50 characters long.", unique=True),
        ),
    ]
