# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0005_auto_20151215_1204'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_viewed_logframe',
            field=models.ForeignKey(to='logframe.LogFrame', null=True),
        ),
    ]
