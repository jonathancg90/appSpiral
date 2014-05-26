# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Brand.entry_id'
        db.delete_column(u'sp_brand', 'entry_id_id')

        # Adding field 'Brand.entry'
        db.add_column(u'sp_brand', 'entry',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='brand_set', to=orm['sp.Entry']),
                      keep_default=False)

        # Deleting field 'CountryHasContract.country_id'
        db.delete_column(u'sp_countryhascontract', 'country_id_id')

        # Deleting field 'CountryHasContract.contract_id'
        db.delete_column(u'sp_countryhascontract', 'contract_id_id')

        # Adding field 'CountryHasContract.country'
        db.add_column(u'sp_countryhascontract', 'country',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Country']),
                      keep_default=False)

        # Adding field 'CountryHasContract.contract'
        db.add_column(u'sp_countryhascontract', 'contract',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Contract']),
                      keep_default=False)

        # Deleting field 'Commercial.brand_id'
        db.delete_column(u'sp_commercial', 'brand_id_id')

        # Deleting field 'Commercial.project_id'
        db.delete_column(u'sp_commercial', 'project_id_id')

        # Adding field 'Commercial.brand'
        db.add_column(u'sp_commercial', 'brand',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='commercial_set', to=orm['sp.Brand']),
                      keep_default=False)

        # Adding field 'Commercial.project'
        db.add_column(u'sp_commercial', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='commercial_set', null=True, to=orm['sp.Project']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Brand.entry_id'
        db.add_column(u'sp_brand', 'entry_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Entry']),
                      keep_default=False)

        # Deleting field 'Brand.entry'
        db.delete_column(u'sp_brand', 'entry_id')

        # Adding field 'CountryHasContract.country_id'
        db.add_column(u'sp_countryhascontract', 'country_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Country']),
                      keep_default=False)

        # Adding field 'CountryHasContract.contract_id'
        db.add_column(u'sp_countryhascontract', 'contract_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Contract']),
                      keep_default=False)

        # Deleting field 'CountryHasContract.country'
        db.delete_column(u'sp_countryhascontract', 'country_id')

        # Deleting field 'CountryHasContract.contract'
        db.delete_column(u'sp_countryhascontract', 'contract_id')

        # Adding field 'Commercial.brand_id'
        db.add_column(u'sp_commercial', 'brand_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sp.Brand']),
                      keep_default=False)

        # Adding field 'Commercial.project_id'
        db.add_column(u'sp_commercial', 'project_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Project'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Commercial.brand'
        db.delete_column(u'sp_commercial', 'brand_id')

        # Deleting field 'Commercial.project'
        db.delete_column(u'sp_commercial', 'project_id')


    models = {
        'sp.brand': {
            'Meta': {'object_name': 'Brand'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brand_set'", 'to': "orm['sp.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.commercial': {
            'Meta': {'object_name': 'Commercial'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commercial_set'", 'to': "orm['sp.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'commercial_set'", 'null': 'True', 'to': "orm['sp.Project']"}),
            'realized': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.contract': {
            'Meta': {'object_name': 'Contract'},
            'character': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ending_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_has_commercial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.ModelHasCommercial']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.countryhascontract': {
            'Meta': {'object_name': 'CountryHasContract'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Contract']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sp.entry': {
            'Meta': {'object_name': 'Entry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.model': {
            'Meta': {'object_name': 'Model'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_code': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sp.modelhascommercial': {
            'Meta': {'object_name': 'ModelHasCommercial'},
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sp.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'project_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'project_type': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['sp']