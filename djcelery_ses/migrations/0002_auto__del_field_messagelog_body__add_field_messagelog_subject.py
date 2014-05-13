# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MessageLog.body'
        db.delete_column(u'djcelery_ses_messagelog', 'body')

        # Adding field 'MessageLog.subject'
        db.add_column(u'djcelery_ses_messagelog', 'subject',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'MessageLog.body'
        db.add_column(u'djcelery_ses_messagelog', 'body',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'MessageLog.subject'
        db.delete_column(u'djcelery_ses_messagelog', 'subject')


    models = {
        u'djcelery_ses.blacklist': {
            'Meta': {'object_name': 'Blacklist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'djcelery_ses.messagelog': {
            'Meta': {'object_name': 'MessageLog'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['djcelery_ses']