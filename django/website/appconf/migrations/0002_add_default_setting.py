# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        orm['appconf.Settings'].objects.create()

    def backwards(self, orm):
        "Write your backwards methods here."
        orm['appconf.Settings'].objects.all().delete()

    models = {
        u'appconf.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_result_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'open_result_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        }
    }

    complete_apps = ['appconf']
    symmetrical = True
