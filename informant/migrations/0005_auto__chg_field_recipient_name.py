# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Recipient.name'
        db.alter_column('informant_recipient', 'name', self.gf('django.db.models.fields.TextField')(max_length=255))
    def backwards(self, orm):

        # Changing field 'Recipient.name'
        db.alter_column('informant_recipient', 'name', self.gf('django.db.models.fields.TextField')())
    models = {
        'informant.newsletter': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Newsletter'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['news.NewsItem']", 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['informant.Recipient']", 'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'informant.recipient': {
            'Meta': {'ordering': "('email',)", 'object_name': 'Recipient'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'news.newsitem': {
            'Meta': {'object_name': 'NewsItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'description_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'h1_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'keywords_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['informant']