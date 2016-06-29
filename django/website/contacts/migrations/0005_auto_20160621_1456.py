# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20160421_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='user',
            field=models.OneToOneField(related_name='_preferences', to=settings.AUTH_USER_MODEL),
        ),
    ]
