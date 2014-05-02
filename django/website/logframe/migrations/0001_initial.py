# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogFrame'
        db.create_table(u'logframe_logframe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['LogFrame'])

        # Adding model 'RiskRating'
        db.create_table(u'logframe_riskrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['RiskRating'])

        # Adding model 'Result'
        db.create_table(u'logframe_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'results', to=orm['logframe.LogFrame'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'children', null=True, to=orm['logframe.Result'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contribution_weighting', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('risk_rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.RiskRating'], null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Rating'], null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'logframe', ['Result'])

        # Adding model 'Assumption'
        db.create_table(u'logframe_assumption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'assumptions', to=orm['logframe.Result'])),
        ))
        db.send_create_signal(u'logframe', ['Assumption'])

        # Adding model 'Indicator'
        db.create_table(u'logframe_indicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'indicators', to=orm['logframe.Result'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'logframe', ['Indicator'])

        # Adding model 'Milestone'
        db.create_table(u'logframe_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.LogFrame'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'logframe', ['Milestone'])

        # Adding model 'SubIndicator'
        db.create_table(u'logframe_subindicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('indicator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'subindicators', to=orm['logframe.Indicator'])),
            ('rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Rating'], null=True, blank=True)),
        ))
        db.send_create_signal(u'logframe', ['SubIndicator'])

        # Adding model 'Column'
        db.create_table(u'logframe_column', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'columns', to=orm['logframe.Indicator'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'logframe', ['Column'])

        # Adding model 'Target'
        db.create_table(u'logframe_target', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('indicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Indicator'])),
            ('subindicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.SubIndicator'], null=True, blank=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Milestone'])),
        ))
        db.send_create_signal(u'logframe', ['Target'])

        # Adding model 'Actual'
        db.create_table(u'logframe_actual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('indicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Indicator'])),
            ('subindicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.SubIndicator'], null=True, blank=True)),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Column'])),
            ('evidence', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'logframe', ['Actual'])

        # Adding model 'Activity'
        db.create_table(u'logframe_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'activities', to=orm['logframe.LogFrame'])),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'activities', to=orm['logframe.Result'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('deliverables', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.User'], null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'logframe', ['Activity'])

        # Adding model 'BudgetLine'
        db.create_table(u'logframe_budgetline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'others', to=orm['logframe.Activity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'logframe', ['BudgetLine'])

        # Adding model 'TAType'
        db.create_table(u'logframe_tatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.LogFrame'])),
        ))
        db.send_create_signal(u'logframe', ['TAType'])

        # Adding model 'TALine'
        db.create_table(u'logframe_taline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'tas', to=orm['logframe.Activity'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.TAType'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('band', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('no_days', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'logframe', ['TALine'])

        # Adding model 'StatusCode'
        db.create_table(u'logframe_statuscode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.LogFrame'])),
        ))
        db.send_create_signal(u'logframe', ['StatusCode'])

        # Adding model 'StatusUpdate'
        db.create_table(u'logframe_statusupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'status_updates', to=orm['logframe.Activity'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.StatusCode'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.User'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'logframe', ['StatusUpdate'])

        # Adding model 'Rating'
        db.create_table(u'logframe_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.LogFrame'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'logframe', ['Rating'])

        # Adding model 'Period'
        db.create_table(u'logframe_period', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.LogFrame'], unique=True)),
            ('start_month', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('num_periods', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
        ))
        db.send_create_signal(u'logframe', ['Period'])


    def backwards(self, orm):
        # Deleting model 'LogFrame'
        db.delete_table(u'logframe_logframe')

        # Deleting model 'RiskRating'
        db.delete_table(u'logframe_riskrating')

        # Deleting model 'Result'
        db.delete_table(u'logframe_result')

        # Deleting model 'Assumption'
        db.delete_table(u'logframe_assumption')

        # Deleting model 'Indicator'
        db.delete_table(u'logframe_indicator')

        # Deleting model 'Milestone'
        db.delete_table(u'logframe_milestone')

        # Deleting model 'SubIndicator'
        db.delete_table(u'logframe_subindicator')

        # Deleting model 'Column'
        db.delete_table(u'logframe_column')

        # Deleting model 'Target'
        db.delete_table(u'logframe_target')

        # Deleting model 'Actual'
        db.delete_table(u'logframe_actual')

        # Deleting model 'Activity'
        db.delete_table(u'logframe_activity')

        # Deleting model 'BudgetLine'
        db.delete_table(u'logframe_budgetline')

        # Deleting model 'TAType'
        db.delete_table(u'logframe_tatype')

        # Deleting model 'TALine'
        db.delete_table(u'logframe_taline')

        # Deleting model 'StatusCode'
        db.delete_table(u'logframe_statuscode')

        # Deleting model 'StatusUpdate'
        db.delete_table(u'logframe_statusupdate')

        # Deleting model 'Rating'
        db.delete_table(u'logframe_rating')

        # Deleting model 'Period'
        db.delete_table(u'logframe_period')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contacts.user': {
            'Meta': {'object_name': 'User'},
            'area_of_specialisation': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'business_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'business_email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'business_tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'home_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home_tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'msn_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'personal_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'yahoo_messenger': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'logframe.activity': {
            'Meta': {'object_name': 'Activity'},
            'deliverables': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contacts.User']", 'null': 'True', 'blank': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'activities'", 'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'activities'", 'to': u"orm['logframe.Result']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'logframe.actual': {
            'Meta': {'object_name': 'Actual'},
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Column']"}),
            'evidence': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Indicator']"}),
            'subindicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.SubIndicator']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'logframe.assumption': {
            'Meta': {'object_name': 'Assumption'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'assumptions'", 'to': u"orm['logframe.Result']"})
        },
        u'logframe.budgetline': {
            'Meta': {'object_name': 'BudgetLine'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'others'", 'to': u"orm['logframe.Activity']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'logframe.column': {
            'Meta': {'object_name': 'Column'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'columns'", 'to': u"orm['logframe.Indicator']"})
        },
        u'logframe.indicator': {
            'Meta': {'object_name': 'Indicator'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'indicators'", 'to': u"orm['logframe.Result']"}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'logframe.logframe': {
            'Meta': {'object_name': 'LogFrame'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.milestone': {
            'Meta': {'ordering': "[u'date']", 'object_name': 'Milestone'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'logframe.period': {
            'Meta': {'object_name': 'Period'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']", 'unique': 'True'}),
            'num_periods': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'start_month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'logframe.rating': {
            'Meta': {'object_name': 'Rating'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'logframe.result': {
            'Meta': {'object_name': 'Result'},
            'contribution_weighting': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.SmallIntegerField', [], {}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'results'", 'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['logframe.Result']"}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Rating']", 'null': 'True', 'blank': 'True'}),
            'risk_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.RiskRating']", 'null': 'True', 'blank': 'True'})
        },
        u'logframe.riskrating': {
            'Meta': {'ordering': "[u'id']", 'object_name': 'RiskRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.statuscode': {
            'Meta': {'ordering': "[u'order']", 'object_name': 'StatusCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'})
        },
        u'logframe.statusupdate': {
            'Meta': {'object_name': 'StatusUpdate'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'status_updates'", 'to': u"orm['logframe.Activity']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.StatusCode']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contacts.User']"})
        },
        u'logframe.subindicator': {
            'Meta': {'ordering': "[u'order']", 'object_name': 'SubIndicator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'subindicators'", 'to': u"orm['logframe.Indicator']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Rating']", 'null': 'True', 'blank': 'True'})
        },
        u'logframe.taline': {
            'Meta': {'object_name': 'TALine'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'tas'", 'to': u"orm['logframe.Activity']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'band': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'no_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.TAType']", 'null': 'True', 'blank': 'True'})
        },
        u'logframe.target': {
            'Meta': {'object_name': 'Target'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Indicator']"}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Milestone']"}),
            'subindicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.SubIndicator']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'logframe.tatype': {
            'Meta': {'ordering': "[u'order']", 'object_name': 'TAType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['logframe']