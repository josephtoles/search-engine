# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Webpage.last_human_request'
        db.alter_column(u'web_webpage', 'last_human_request', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Webpage.last_human_request'
        db.alter_column(u'web_webpage', 'last_human_request', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 22, 0, 0)))

    models = {
        u'web.webpage': {
            'Meta': {'ordering': "['url']", 'unique_together': "(['url', 'website'],)", 'object_name': 'Webpage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_human_request': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
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