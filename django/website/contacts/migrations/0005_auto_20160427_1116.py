# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def delete_south_permissions(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    Permission.objects.filter(codename__endswith='migrationhistory').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20160421_1645'),
    ]

    operations = [
        migrations.RunPython(delete_south_permissions)
    ]
