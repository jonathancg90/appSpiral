# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyDetailAccount'
        db.create_table(u'sp_companydetailaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company_detail_account_set', to=orm['sp.Bank'])),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('sp', ['CompanyDetailAccount'])

        # Adding model 'Bank'
        db.create_table(u'sp_bank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('sp', ['Bank'])

        # Adding model 'Company'
        db.create_table(u'sp_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('ruc', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('sp', ['Company'])

        # Adding model 'CommercialDateDetail'
        db.create_table(u'sp_commercialdatedetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commercial', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company_detail_account_set', to=orm['sp.Commercial'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('sp', ['CommercialDateDetail'])

        # Deleting field 'Project.project_name'
        db.delete_column(u'sp_project', 'project_name')

        # Deleting field 'Project.project_type'
        db.delete_column(u'sp_project', 'project_type')

        # Adding field 'Project.line_productions'
        db.add_column(u'sp_project', 'line_productions',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Project.commercial'
        db.add_column(u'sp_project', 'commercial',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_set', null=True, to=orm['sp.Commercial']),
                      keep_default=False)

        # Adding field 'Project.start_productions'
        db.add_column(u'sp_project', 'start_productions',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 27, 0, 0)),
                      keep_default=False)

        # Adding field 'Project.end_productions'
        db.add_column(u'sp_project', 'end_productions',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 27, 0, 0)),
                      keep_default=False)

        # Adding field 'Project.budget'
        db.add_column(u'sp_project', 'budget',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.budget_cost'
        db.add_column(u'sp_project', 'budget_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.observations'
        db.add_column(u'sp_project', 'observations',
                      self.gf('django.db.models.fields.TextField')(default=0),
                      keep_default=False)

        # Adding field 'Project.status'
        db.add_column(u'sp_project', 'status',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CompanyDetailAccount'
        db.delete_table(u'sp_companydetailaccount')

        # Deleting model 'Bank'
        db.delete_table(u'sp_bank')

        # Deleting model 'Company'
        db.delete_table(u'sp_company')

        # Deleting model 'CommercialDateDetail'
        db.delete_table(u'sp_commercialdatedetail')

        # Adding field 'Project.project_name'
        db.add_column(u'sp_project', 'project_name',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=45),
                      keep_default=False)

        # Adding field 'Project.project_type'
        db.add_column(u'sp_project', 'project_type',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Project.line_productions'
        db.delete_column(u'sp_project', 'line_productions')

        # Deleting field 'Project.commercial'
        db.delete_column(u'sp_project', 'commercial_id')

        # Deleting field 'Project.start_productions'
        db.delete_column(u'sp_project', 'start_productions')

        # Deleting field 'Project.end_productions'
        db.delete_column(u'sp_project', 'end_productions')

        # Deleting field 'Project.budget'
        db.delete_column(u'sp_project', 'budget')

        # Deleting field 'Project.budget_cost'
        db.delete_column(u'sp_project', 'budget_cost')

        # Deleting field 'Project.observations'
        db.delete_column(u'sp_project', 'observations')

        # Deleting field 'Project.status'
        db.delete_column(u'sp_project', 'status')


    models = {
        'sp.bank': {
            'Meta': {'object_name': 'Bank'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
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
        'sp.commercialdatedetail': {
            'Meta': {'object_name': 'CommercialDateDetail'},
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_detail_account_set'", 'to': "orm['sp.Commercial']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sp.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'ruc': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.companydetailaccount': {
            'Meta': {'object_name': 'CompanyDetailAccount'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_detail_account_set'", 'to': "orm['sp.Bank']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_set'", 'null': 'True', 'to': "orm['sp.City']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True'}),
            'feature_detail': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.FeatureValue']", 'through': "orm['sp.ModelFeatureDetail']", 'symmetrical': 'False'}),
            'gender': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'main_image': ('django.db.models.fields.CharField', [], {'default': "'img/default.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'model_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name_complete': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_set'", 'null': 'True', 'to': "orm['sp.Country']"}),
            'number_doc': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True'}),
            'phone_fixed': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'phone_mobil': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_doc': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'sp.modelfeaturedetail': {
            'Meta': {'object_name': 'ModelFeatureDetail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'feature_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_feature_detail_set'", 'to': "orm['sp.FeatureValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_feature_detail_set'", 'to': "orm['sp.Model']"}),
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
            'budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'budget_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_set'", 'null': 'True', 'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_productions': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_productions': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {}),
            'project_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'start_productions': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['sp']