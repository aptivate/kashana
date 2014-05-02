# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Settings'
        db.create_table(u'appconf_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('max_result_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
            ('open_result_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
        ))
        db.send_create_signal(u'appconf', ['Settings'])


    def backwards(self, orm):
        # Deleting model 'Settings'
        db.delete_table(u'appconf_settings')


    models = {
        u'appconf.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_result_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'open_result_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        }
    }

    complete_apps = ['appconf']