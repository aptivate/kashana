# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_user_profiles(apps, schema_editor):
    User = apps.get_model('contacts', 'User')
    UserPreferences = apps.get_model('contacts', 'UserPreferences')

    for user in User.objects.all():
        UserPreferences.objects.create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20160420_1628'),
    ]

    operations = [
        migrations.RunPython(add_user_profiles)
    ]
