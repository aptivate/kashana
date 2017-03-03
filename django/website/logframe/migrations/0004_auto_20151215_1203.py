# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import migrations, models
from django.utils.text import slugify


def set_logframe_slug(apps, schema_editor):
    LogFrame = apps.get_model('logframe', 'LogFrame')
    for logframe in LogFrame.objects.all():
        count = LogFrame.objects.filter(slug__startswith=logframe.slug[:46]).count()

        max_length = LogFrame._meta.get_field('slug').max_length
        base_slug = slugify(logframe.name.lower())
        slug = base_slug[:max_length]

        while LogFrame.objects.filter(slug=slug).exists():
            # Based on https://keyerror.com/blog/automatically-generating-unique-slugs-in-django at 03/03/2017
            count += 1
            slug = '{0}{1:d}'.format(base_slug[:max_length - len(unicode(count))], count)

        logframe.slug = slug
        logframe.save()


class Migration(migrations.Migration):

    dependencies = [
        ('logframe', '0003_logframe_slug'),
    ]

    operations = [
        migrations.RunPython(set_logframe_slug)
    ]
