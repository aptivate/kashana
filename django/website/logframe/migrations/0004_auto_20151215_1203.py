# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import migrations, models


def set_logframe_slug(apps, schema_editor):
    LogFrame = apps.get_model('logframe', 'LogFrame')
    for logframe in LogFrame.objects.all():
        slug = logframe.name.lower()
        slug.replace(' ', '_')
        slug = re.sub('[^\w-]', '', slug)
        slug = slug[:47]
        if LogFrame.objects.filter(slug=slug).exists():
            count = LogFrame.objects.filter(slug__startswith=slug).count() + 1
            slug += unicode(count)
        logframe.slug = slug
        logframe.save()


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0003_logframe_slug'),
    ]

    operations = [
        migrations.RunPython(set_logframe_slug)
    ]
