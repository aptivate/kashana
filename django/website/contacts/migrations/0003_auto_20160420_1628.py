# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0005_auto_20151215_1204'),
        ('contacts', '0002_user_last_viewed_logframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_viewed_logframe', models.ForeignKey(to='logframe.LogFrame', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_viewed_logframe',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='user',
            field=models.OneToOneField(related_name='preferences', to=settings.AUTH_USER_MODEL),
        ),
    ]
