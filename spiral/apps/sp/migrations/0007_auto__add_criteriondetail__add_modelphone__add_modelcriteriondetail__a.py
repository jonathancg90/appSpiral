# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CriterionDetail'
        db.create_table(u'sp_criteriondetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('criterion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criterion_detail_set', to=orm['sp.Criterion'])),
            ('cri_item', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['CriterionDetail'])

        # Adding model 'ModelPhone'
        db.create_table(u'sp_modelphone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model_phone_set', to=orm['sp.Model'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=4)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('sp', ['ModelPhone'])

        # Adding model 'ModelCriterionDetail'
        db.create_table(u'sp_modelcriteriondetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model_criterion_detail_set', to=orm['sp.Model'])),
            ('criterion_detail', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model_criterion_detail_set', to=orm['sp.CriterionDetail'])),
            ('observations', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('level', self.gf('django.db.models.fields.SmallIntegerField')(default=None, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['ModelCriterionDetail'])

        # Adding model 'Criterion'
        db.create_table(u'sp_criterion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cri_cod', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('criterion_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criterion_set', to=orm['sp.CriterionCategory'])),
            ('multi', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['Criterion'])

        # Adding model 'CriterionCategory'
        db.create_table(u'sp_criterioncategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['CriterionCategory'])

        # Adding field 'Model.dni'
        db.add_column(u'sp_model', 'dni',
                      self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True),
                      keep_default=False)

        # Adding field 'Model.status'
        db.add_column(u'sp_model', 'status',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Model.name'
        db.add_column(u'sp_model', 'name',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=45),
                      keep_default=False)

        # Adding field 'Model.last_name'
        db.add_column(u'sp_model', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=45),
                      keep_default=False)

        # Adding field 'Model.alias'
        db.add_column(u'sp_model', 'alias',
                      self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Model.address'
        db.add_column(u'sp_model', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Model.reference'
        db.add_column(u'sp_model', 'reference',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Model.email'
        db.add_column(u'sp_model', 'email',
                      self.gf('django.db.models.fields.EmailField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Model.birth'
        db.add_column(u'sp_model', 'birth',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 16, 0, 0)),
                      keep_default=False)

        # Adding field 'Model.birth_place'
        db.add_column(u'sp_model', 'birth_place',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Model.height'
        db.add_column(u'sp_model', 'height',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Model.weight'
        db.add_column(u'sp_model', 'weight',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Model.size_shoe'
        db.add_column(u'sp_model', 'size_shoe',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Model.experience'
        db.add_column(u'sp_model', 'experience',
                      self.gf('django.db.models.fields.CharField')(default=u'Ninguna', max_length=300),
                      keep_default=False)

        # Adding field 'Model.last_visit'
        db.add_column(u'sp_model', 'last_visit',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding unique constraint on 'Model', fields ['model_code']
        db.create_unique(u'sp_model', ['model_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Model', fields ['model_code']
        db.delete_unique(u'sp_model', ['model_code'])

        # Deleting model 'CriterionDetail'
        db.delete_table(u'sp_criteriondetail')

        # Deleting model 'ModelPhone'
        db.delete_table(u'sp_modelphone')

        # Deleting model 'ModelCriterionDetail'
        db.delete_table(u'sp_modelcriteriondetail')

        # Deleting model 'Criterion'
        db.delete_table(u'sp_criterion')

        # Deleting model 'CriterionCategory'
        db.delete_table(u'sp_criterioncategory')

        # Deleting field 'Model.dni'
        db.delete_column(u'sp_model', 'dni')

        # Deleting field 'Model.status'
        db.delete_column(u'sp_model', 'status')

        # Deleting field 'Model.name'
        db.delete_column(u'sp_model', 'name')

        # Deleting field 'Model.last_name'
        db.delete_column(u'sp_model', 'last_name')

        # Deleting field 'Model.alias'
        db.delete_column(u'sp_model', 'alias')

        # Deleting field 'Model.address'
        db.delete_column(u'sp_model', 'address')

        # Deleting field 'Model.reference'
        db.delete_column(u'sp_model', 'reference')

        # Deleting field 'Model.email'
        db.delete_column(u'sp_model', 'email')

        # Deleting field 'Model.birth'
        db.delete_column(u'sp_model', 'birth')

        # Deleting field 'Model.birth_place'
        db.delete_column(u'sp_model', 'birth_place')

        # Deleting field 'Model.height'
        db.delete_column(u'sp_model', 'height')

        # Deleting field 'Model.weight'
        db.delete_column(u'sp_model', 'weight')

        # Deleting field 'Model.size_shoe'
        db.delete_column(u'sp_model', 'size_shoe')

        # Deleting field 'Model.experience'
        db.delete_column(u'sp_model', 'experience')

        # Deleting field 'Model.last_visit'
        db.delete_column(u'sp_model', 'last_visit')


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
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.countryhascontract': {
            'Meta': {'object_name': 'CountryHasContract'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Contract']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sp.criterion': {
            'Meta': {'object_name': 'Criterion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cri_cod': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'criterion_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criterion_set'", 'to': "orm['sp.CriterionCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'multi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.criterioncategory': {
            'Meta': {'object_name': 'CriterionCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.criteriondetail': {
            'Meta': {'object_name': 'CriterionDetail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cri_item': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criterion_detail_set'", 'to': "orm['sp.Criterion']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True'}),
            'experience': ('django.db.models.fields.CharField', [], {'default': "u'Ninguna'", 'max_length': '300'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'last_visit': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'model_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'size_shoe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'sp.modelcriteriondetail': {
            'Meta': {'object_name': 'ModelCriterionDetail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion_detail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_criterion_detail_set'", 'to': "orm['sp.CriterionDetail']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_criterion_detail_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'sp.modelhascommercial': {
            'Meta': {'object_name': 'ModelHasCommercial'},
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sp.modelphone': {
            'Meta': {'object_name': 'ModelPhone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_phone_set'", 'to': "orm['sp.Model']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'})
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