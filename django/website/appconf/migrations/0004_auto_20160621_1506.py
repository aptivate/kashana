# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0003_add_logframe_to_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='logframe',
            field=models.OneToOneField(to='logframe.LogFrame'),
        ),
    ]
