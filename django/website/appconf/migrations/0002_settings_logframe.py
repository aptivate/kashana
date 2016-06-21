# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0006_auto_20160427_0932'),
        ('appconf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='logframe',
            field=models.OneToOneField(null=True, to='logframe.LogFrame'),
        ),
    ]
