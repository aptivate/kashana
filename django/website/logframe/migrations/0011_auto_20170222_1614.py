# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0010_auto_20170222_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logframe',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
        ),
    ]
