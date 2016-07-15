# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20160621_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='area_of_specialisation',
        ),
        migrations.RemoveField(
            model_name='user',
            name='business_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='business_tel',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact_type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cv',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_tel',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job_title',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='msn_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='user',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='user',
            name='personal_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='user',
            name='skype_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='title',
        ),
        migrations.RemoveField(
            model_name='user',
            name='yahoo_messenger',
        ),
    ]
