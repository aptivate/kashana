# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import logframe.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('deliverables', models.TextField(blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('order', models.IntegerField()),
                ('lead', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Actual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=200, blank=True)),
                ('evidence', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Assumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('amount', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('activity', models.ForeignKey(related_name='others', to='logframe.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('source', models.TextField(null=True, blank=True)),
            ],
            bases=(logframe.models.AverageTargetPercentMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LogFrame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Log Frame', unique=True, max_length=255)),
            ],
            bases=(logframe.models.AverageTargetPercentMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('log_frame', models.ForeignKey(to='logframe.LogFrame')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_month', models.PositiveSmallIntegerField(default=1, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('num_periods', models.PositiveSmallIntegerField(default=4, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (6, 6)])),
                ('log_frame', models.OneToOneField(to='logframe.LogFrame')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('color', models.CharField(max_length=32, choices=[('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('lightest-grey', 'Lightest grey'), ('light-grey', 'Light grey'), ('grey', 'Grey')])),
                ('log_frame', models.ForeignKey(to='logframe.LogFrame')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('contribution_weighting', models.IntegerField(default=0)),
                ('level', models.SmallIntegerField(default=0)),
                ('order', models.IntegerField()),
                ('log_frame', models.ForeignKey(related_name='results', to='logframe.LogFrame')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='logframe.Result', null=True)),
                ('rating', models.ForeignKey(blank=True, to='logframe.Rating', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RiskRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='StatusCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(help_text='Set automatically when not specified.', blank=True)),
                ('log_frame', models.ForeignKey(to='logframe.LogFrame')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('activity', models.ForeignKey(related_name='status_updates', to='logframe.Activity')),
                ('code', models.ForeignKey(blank=True, to='logframe.StatusCode', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(help_text='Set automatically when not specified.', blank=True)),
                ('indicator', models.ForeignKey(related_name='subindicators', to='logframe.Indicator')),
                ('rating', models.ForeignKey(blank=True, to='logframe.Rating', null=True)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TALine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('band', models.CharField(max_length=10, null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('no_days', models.IntegerField(null=True, blank=True)),
                ('amount', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('activity', models.ForeignKey(related_name='tas', to='logframe.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=200, blank=True)),
                ('indicator', models.ForeignKey(to='logframe.Indicator')),
                ('milestone', models.ForeignKey(to='logframe.Milestone')),
                ('subindicator', models.ForeignKey(blank=True, to='logframe.SubIndicator', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TAType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(help_text='Set automatically when not specified.', blank=True)),
                ('log_frame', models.ForeignKey(to='logframe.LogFrame')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='taline',
            name='type',
            field=models.ForeignKey(blank=True, to='logframe.TAType', null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='risk_rating',
            field=models.ForeignKey(blank=True, to='logframe.RiskRating', null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='result',
            field=models.ForeignKey(related_name='indicators', to='logframe.Result'),
        ),
        migrations.AddField(
            model_name='column',
            name='indicator',
            field=models.ForeignKey(related_name='columns', to='logframe.Indicator'),
        ),
        migrations.AddField(
            model_name='assumption',
            name='result',
            field=models.ForeignKey(related_name='assumptions', to='logframe.Result'),
        ),
        migrations.AddField(
            model_name='actual',
            name='column',
            field=models.ForeignKey(to='logframe.Column'),
        ),
        migrations.AddField(
            model_name='actual',
            name='indicator',
            field=models.ForeignKey(to='logframe.Indicator'),
        ),
        migrations.AddField(
            model_name='actual',
            name='subindicator',
            field=models.ForeignKey(blank=True, to='logframe.SubIndicator', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='log_frame',
            field=models.ForeignKey(related_name='activities', to='logframe.LogFrame'),
        ),
        migrations.AddField(
            model_name='activity',
            name='result',
            field=models.ForeignKey(related_name='activities', to='logframe.Result'),
        ),
    ]
