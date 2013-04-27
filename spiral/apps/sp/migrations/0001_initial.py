# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rubro'
        db.create_table(u'sp_rubro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('sp', ['Rubro'])

        # Adding model 'Marca'
        db.create_table(u'sp_marca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('rubro_idrubro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Rubro'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('sp', ['Marca'])

        # Adding model 'ModeloHasContrato'
        db.create_table(u'sp_modelohascontrato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sp', ['ModeloHasContrato'])

        # Adding model 'Comercial'
        db.create_table(u'sp_comercial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('realizado', self.gf('django.db.models.fields.DateTimeField')()),
            ('marcas_idmarcas', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Marca'])),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('modelo_has_contratos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.ModeloHasContrato'])),
        ))
        db.send_create_signal('sp', ['Comercial'])

        # Adding model 'Contrato'
        db.create_table(u'sp_contrato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ending_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('comercial_idcomercial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sp.Comercial'])),
        ))
        db.send_create_signal('sp', ['Contrato'])


    def backwards(self, orm):
        # Deleting model 'Rubro'
        db.delete_table(u'sp_rubro')

        # Deleting model 'Marca'
        db.delete_table(u'sp_marca')

        # Deleting model 'ModeloHasContrato'
        db.delete_table(u'sp_modelohascontrato')

        # Deleting model 'Comercial'
        db.delete_table(u'sp_comercial')

        # Deleting model 'Contrato'
        db.delete_table(u'sp_contrato')


    models = {
        'sp.comercial': {
            'Meta': {'object_name': 'Comercial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marcas_idmarcas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Marca']"}),
            'modelo_has_contratos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.ModeloHasContrato']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'realizado': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'comercial_idcomercial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Comercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ending_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.marca': {
            'Meta': {'object_name': 'Marca'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'rubro_idrubro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.Rubro']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.modelohascontrato': {
            'Meta': {'object_name': 'ModeloHasContrato'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {})
        },
        'sp.rubro': {
            'Meta': {'object_name': 'Rubro'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['sp']