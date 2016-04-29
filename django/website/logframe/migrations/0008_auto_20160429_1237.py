# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0007_auto_20160425_1155'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resultlevelname',
            unique_together=set([('level_number', 'logframe')]),
        ),
    ]
