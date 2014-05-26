# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ModelPhone'
        db.delete_table(u'sp_modelphone')

        # Adding model 'FeatureValue'
        db.create_table(u'sp_featurevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feature_value_set', to=orm['sp.Feature'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('sp', ['FeatureValue'])

        # Adding model 'City'
        db.create_table(u'sp_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='city_set', to=orm['sp.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['City'])

        # Deleting field 'Model.dni'
        db.delete_column(u'sp_model', 'dni')

        # Deleting field 'Model.experience'
        db.delete_column(u'sp_model', 'experience')

        # Deleting field 'Model.birth_place'
        db.delete_column(u'sp_model', 'birth_place')

        # Deleting field 'Model.size_shoe'
        db.delete_column(u'sp_model', 'size_shoe')

        # Deleting field 'Model.reference'
        db.delete_column(u'sp_model', 'reference')

        # Adding field 'Model.type_doc'
        db.add_column(u'sp_model', 'type_doc',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Model.number_doc'
        db.add_column(u'sp_model', 'number_doc',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'Model.gender'
        db.add_column(u'sp_model', 'gender',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Model.nationality'
        db.add_column(u'sp_model', 'nationality',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='model_set', null=True, to=orm['sp.Country']),
                      keep_default=False)

        # Adding field 'Model.phone_fixed'
        db.add_column(u'sp_model', 'phone_fixed',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Model.phone_mobil'
        db.add_column(u'sp_model', 'phone_mobil',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.nationality'
        db.add_column(u'sp_country', 'nationality',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=45),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ModelPhone'
        db.create_table(u'sp_modelphone', (
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model_phone_set', to=orm['sp.Model'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=4)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('sp', ['ModelPhone'])

        # Deleting model 'FeatureValue'
        db.delete_table(u'sp_featurevalue')

        # Deleting model 'City'
        db.delete_table(u'sp_city')

        # Adding field 'Model.dni'
        db.add_column(u'sp_model', 'dni',
                      self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, null=True),
                      keep_default=False)

        # Adding field 'Model.experience'
        db.add_column(u'sp_model', 'experience',
                      self.gf('django.db.models.fields.CharField')(default=u'Ninguna', max_length=300),
                      keep_default=False)

        # Adding field 'Model.birth_place'
        db.add_column(u'sp_model', 'birth_place',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Model.size_shoe'
        db.add_column(u'sp_model', 'size_shoe',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Model.reference'
        db.add_column(u'sp_model', 'reference',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Model.type_doc'
        db.delete_column(u'sp_model', 'type_doc')

        # Deleting field 'Model.number_doc'
        db.delete_column(u'sp_model', 'number_doc')

        # Deleting field 'Model.gender'
        db.delete_column(u'sp_model', 'gender')

        # Deleting field 'Model.nationality'
        db.delete_column(u'sp_model', 'nationality_id')

        # Deleting field 'Model.phone_fixed'
        db.delete_column(u'sp_model', 'phone_fixed')

        # Deleting field 'Model.phone_mobil'
        db.delete_column(u'sp_model', 'phone_mobil')

        # Deleting field 'Country.nationality'
        db.delete_column(u'sp_country', 'nationality')


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
        'sp.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'city_set'", 'to': "orm['sp.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_has_commercial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.ModelHasCommercial']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'period_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
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
        'sp.feature': {
            'Meta': {'object_name': 'Feature'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.featurevalue': {
            'Meta': {'object_name': 'FeatureValue'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feature_value_set'", 'to': "orm['sp.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.model': {
            'Meta': {'object_name': 'Model'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True'}),
            'gender': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'last_visit': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'model_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_set'", 'null': 'True', 'to': "orm['sp.Country']"}),
            'number_doc': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'phone_fixed': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'phone_mobil': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type_doc': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
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