# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Contrato'
        db.delete_table(u'sp_contrato')

        # Deleting model 'Marca'
        db.delete_table(u'sp_marca')

        # Deleting model 'ModeloHasContrato'
        db.delete_table(u'sp_modelohascontrato')

        # Deleting model 'Comercial'
        db.delete_table(u'sp_comercial')

        # Deleting model 'Rubro'
        db.delete_table(u'sp_rubro')

        # Adding model 'Brand'
        db.create_table(u'sp_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('entry_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Entry'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('sp', ['Brand'])

        # Adding model 'ModelHasCommercial'
        db.create_table(u'sp_modelhascommercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Model'])),
            ('commercial_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Commercial'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['ModelHasCommercial'])

        # Adding model 'Commercial'
        db.create_table(u'sp_commercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('realized', self.gf('django.db.models.fields.DateTimeField')()),
            ('brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Brand'])),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Project'])),
        ))
        db.send_create_signal('sp', ['Commercial'])

        # Adding model 'Project'
        db.create_table(u'sp_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('project_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['Project'])

        # Adding model 'Contract'
        db.create_table(u'sp_contract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ending_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('model_has_commercial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.ModelHasCommercial'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('character', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('sp', ['Contract'])

        # Adding model 'Entry'
        db.create_table(u'sp_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('sp', ['Entry'])

        # Adding model 'Model'
        db.create_table(u'sp_model', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_code', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['Model'])


    def backwards(self, orm):
        # Adding model 'Contrato'
        db.create_table(u'sp_contrato', (
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('comercial_idcomercial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Comercial'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ending_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sp', ['Contrato'])

        # Adding model 'Marca'
        db.create_table(u'sp_marca', (
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('rubro_idrubro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Rubro'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=45)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sp', ['Marca'])

        # Adding model 'ModeloHasContrato'
        db.create_table(u'sp_modelohascontrato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sp', ['ModeloHasContrato'])

        # Adding model 'Comercial'
        db.create_table(u'sp_comercial', (
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('marcas_idmarcas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Marca'])),
            ('modelo_has_contratos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.ModeloHasContrato'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('realizado', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sp', ['Comercial'])

        # Adding model 'Rubro'
        db.create_table(u'sp_rubro', (
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=45)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sp', ['Rubro'])

        # Deleting model 'Brand'
        db.delete_table(u'sp_brand')

        # Deleting model 'ModelHasCommercial'
        db.delete_table(u'sp_modelhascommercial')

        # Deleting model 'Commercial'
        db.delete_table(u'sp_commercial')

        # Deleting model 'Project'
        db.delete_table(u'sp_project')

        # Deleting model 'Contract'
        db.delete_table(u'sp_contract')

        # Deleting model 'Entry'
        db.delete_table(u'sp_entry')

        # Deleting model 'Model'
        db.delete_table(u'sp_model')


    models = {
        'sp.brand': {
            'Meta': {'object_name': 'Brand'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.commercial': {
            'Meta': {'object_name': 'Commercial'},
            'brand_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Project']"}),
            'realized': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
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
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.entry': {
            'Meta': {'object_name': 'Entry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
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
            'commercial_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sp.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'project_type': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['sp']