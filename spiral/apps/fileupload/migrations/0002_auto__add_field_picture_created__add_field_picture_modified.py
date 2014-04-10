# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Picture.created'
        db.add_column(u'fileupload_picture', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date.today(), blank=True),
                      keep_default=False)

        # Adding field 'Picture.modified'
        db.add_column(u'fileupload_picture', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date.today(), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Picture.created'
        db.delete_column(u'fileupload_picture', 'created')

        # Deleting field 'Picture.modified'
        db.delete_column(u'fileupload_picture', 'modified')


    models = {
        u'fileupload.picture': {
            'Meta': {'object_name': 'Picture'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['fileupload']