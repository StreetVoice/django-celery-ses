# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Blacklist'
        db.create_table(u'svcelery_email_blacklist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'svcelery_email', ['Blacklist'])

        # Adding model 'MessageLog'
        db.create_table(u'svcelery_email_messagelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'svcelery_email', ['MessageLog'])


    def backwards(self, orm):
        # Deleting model 'Blacklist'
        db.delete_table(u'svcelery_email_blacklist')

        # Deleting model 'MessageLog'
        db.delete_table(u'svcelery_email_messagelog')


    models = {
        u'svcelery_email.blacklist': {
            'Meta': {'object_name': 'Blacklist'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'svcelery_email.messagelog': {
            'Meta': {'object_name': 'MessageLog'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['svcelery_email']