# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field recipient on 'Newsletter'
        db.create_table('informant_newsletter_recipient', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['informant.newsletter'], null=False)),
            ('recipient', models.ForeignKey(orm['informant.recipient'], null=False))
        ))
        db.create_unique('informant_newsletter_recipient', ['newsletter_id', 'recipient_id'])

    def backwards(self, orm):
        # Removing M2M table for field recipient on 'Newsletter'
        db.delete_table('informant_newsletter_recipient')

    models = {
        'informant.newsletter': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Newsletter'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['informant']