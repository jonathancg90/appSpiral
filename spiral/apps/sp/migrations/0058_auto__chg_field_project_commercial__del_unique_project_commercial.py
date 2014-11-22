# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Project', fields ['commercial']
        db.delete_unique(u'sp_project', ['commercial_id'])


        # Changing field 'Project.commercial'
        db.alter_column(u'sp_project', 'commercial_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sp.Commercial']))

    def backwards(self, orm):

        # Changing field 'Project.commercial'
        db.alter_column(u'sp_project', 'commercial_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['sp.Commercial']))
        # Adding unique constraint on 'Project', fields ['commercial']
        db.create_unique(u'sp_project', ['commercial_id'])


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
        'sp.broadcast': {
            'Meta': {'object_name': 'Broadcast'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.casting': {
            'Meta': {'object_name': 'Casting'},
            'ppg': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ppi': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'type_casting': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.TypeCasting']", 'symmetrical': 'False'})
        },
        'sp.castingdetailmodel': {
            'Meta': {'object_name': 'CastingDetailModel'},
            'budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'casting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'casting_detail_model_set'", 'to': "orm['sp.Casting']"}),
            'character': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'scene': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'type_casting': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.TypeCasting']", 'null': 'True', 'symmetrical': 'False'})
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
        'sp.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'ruc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type_client': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.TypeClient']", 'symmetrical': 'False'})
        },
        'sp.commercial': {
            'Meta': {'object_name': 'Commercial'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commercial_set'", 'to': "orm['sp.Brand']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.commercialdatedetail': {
            'Meta': {'object_name': 'CommercialDateDetail'},
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commercial_date_detail_set'", 'to': "orm['sp.Commercial']"}),
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
        'sp.currency': {
            'Meta': {'object_name': 'Currency'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'sp.dutydetail': {
            'Meta': {'object_name': 'DutyDetail'},
            'broadcast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.Broadcast']", 'null': 'True', 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.Country']", 'null': 'True', 'symmetrical': 'False'}),
            'duration_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'type_contract': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'duty_detail_set'", 'null': 'True', 'to': "orm['sp.TypeContract']"})
        },
        'sp.entry': {
            'Meta': {'object_name': 'Entry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.extras': {
            'Meta': {'object_name': 'Extras'},
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sp.extrasdetailmodel': {
            'Meta': {'object_name': 'ExtrasDetailModel'},
            'budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'budget_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'character': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_detail_set'", 'null': 'True', 'to': "orm['sp.Currency']"}),
            'extras': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extras_detail_model_set'", 'to': "orm['sp.Extras']"}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'schedule': ('django.db.models.fields.TextField', [], {'null': 'True'})
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
        'sp.payment': {
            'Meta': {'object_name': 'Payment'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'casting_set'", 'null': 'True', 'to': "orm['sp.Client']"}),
            'conditions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sp.photocasting': {
            'Meta': {'object_name': 'PhotoCasting'},
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'type_casting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_set'", 'to': "orm['sp.TypePhotoCasting']"}),
            'use_photo': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.UsePhotos']", 'symmetrical': 'False'})
        },
        'sp.photocastingdetailmodel': {
            'Meta': {'object_name': 'PhotoCastingDetailModel'},
            'budget_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'character': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_detail_model_set'", 'null': 'True', 'to': "orm['sp.Currency']"}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'photo_casting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_detail_model_set'", 'to': "orm['sp.PhotoCasting']"}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.project': {
            'Meta': {'object_name': 'Project'},
            'budget': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'budget_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'client': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.Client']", 'through': "orm['sp.ProjectClientDetail']", 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_set'", 'null': 'True', 'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_set'", 'null': 'True', 'to': "orm['sp.Currency']"}),
            'end_productions': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_productions': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'start_productions': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sp.projectclientdetail': {
            'Meta': {'object_name': 'ProjectClientDetail'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Project']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.TypeClient']"})
        },
        'sp.projectdetaildeliveries': {
            'Meta': {'object_name': 'ProjectDetailDeliveries'},
            'delivery_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_detail_deliveries_set'", 'null': 'True', 'to': "orm['sp.Project']"})
        },
        'sp.projectdetailstaff': {
            'Meta': {'object_name': 'ProjectDetailStaff'},
            'budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'percentage': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_detail_staff_set'", 'null': 'True', 'to': "orm['sp.Project']"}),
            'role': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.projectdetailstudio': {
            'Meta': {'object_name': 'ProjectDetailStudio'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_detail_studio_set'", 'null': 'True', 'to': "orm['sp.Project']"}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_detail_studio_set'", 'null': 'True', 'to': "orm['sp.Studio']"})
        },
        'sp.representation': {
            'Meta': {'object_name': 'Representation'},
            'ppg': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ppi': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sp.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'type_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_set'", 'null': 'True', 'to': "orm['sp.TypeEvent']"})
        },
        'sp.representationdetailmodel': {
            'Meta': {'object_name': 'RepresentationDetailModel'},
            'budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'budget_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'character': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_detail_model_set'", 'null': 'True', 'to': "orm['sp.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_detail_model_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'representation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_detail_model_set'", 'to': "orm['sp.Representation']"}),
            'schedule': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'sp.studio': {
            'Meta': {'object_name': 'Studio'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typecasting': {
            'Meta': {'object_name': 'TypeCasting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typeclient': {
            'Meta': {'object_name': 'TypeClient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'sp.typecontract': {
            'Meta': {'object_name': 'TypeContract'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typeevent': {
            'Meta': {'object_name': 'TypeEvent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typephotocasting': {
            'Meta': {'object_name': 'TypePhotoCasting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.usephotos': {
            'Meta': {'object_name': 'UsePhotos'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['sp']