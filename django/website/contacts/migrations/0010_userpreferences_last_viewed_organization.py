# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_model_update'),
        ('contacts', '0009_assign_default_orgranisations'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='last_viewed_organization',
            field=models.ForeignKey(to='organizations.Organization', null=True),
        ),
    ]
