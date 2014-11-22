# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Webpage', fields ['url']
        db.delete_unique(u'web_webpage', ['url'])

        # Adding unique constraint on 'Webpage', fields ['url', 'website']
        db.create_unique(u'web_webpage', ['url', 'website_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Webpage', fields ['url', 'website']
        db.delete_unique(u'web_webpage', ['url', 'website_id'])

        # Adding unique constraint on 'Webpage', fields ['url']
        db.create_unique(u'web_webpage', ['url'])


    models = {
        u'web.webpage': {
            'Meta': {'ordering': "['url']", 'unique_together': "(['url', 'website'],)", 'object_name': 'Webpage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'robots_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Website']"})
        },
        u'web.website': {
            'Meta': {'ordering': "['url']", 'object_name': 'Website'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'robots_content': ('django.db.models.fields.TextField', [], {}),
            'robots_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'robots_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['web']