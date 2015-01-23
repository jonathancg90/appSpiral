# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Support'
        db.create_table(u'sp_support', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('sp', ['Support'])


    def backwards(self, orm):
        # Deleting model 'Support'
        db.delete_table(u'sp_support')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fileupload.picture': {
            'Meta': {'object_name': 'Picture'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'taken_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'realized': ('django.db.models.fields.DateField', [], {'null': 'True'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'scene': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'type_casting': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.TypeCasting']", 'null': 'True', 'symmetrical': 'False'})
        },
        'sp.castingdetailparticipate': {
            'Meta': {'object_name': 'CastingDetailParticipate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'casting_detail_participate_set'", 'to': "orm['sp.CastingDetailModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'casting_detail_participate_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'sp.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'city_set'", 'to': "orm['sp.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'broadcast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.Broadcast']", 'null': 'True', 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sp.Country']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_contract': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'period_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_contract': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type_contract': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contract_set'", 'null': 'True', 'to': "orm['sp.TypeContract']"})
        },
        'sp.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.currency': {
            'Meta': {'object_name': 'Currency'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'sp.detaillist': {
            'DNI': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'Meta': {'object_name': 'DetailList'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.List']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'detail_list_set'", 'null': 'True', 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name_complete': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'sp.detailpauta': {
            'Meta': {'object_name': 'DetailPauta'},
            'character': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hour': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'detail_pauta_set'", 'null': 'True', 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'pauta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'detail_pauta_set'", 'to': "orm['sp.Pauta']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.extradetailparticipate': {
            'Meta': {'object_name': 'ExtraDetailParticipate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_detail_participate_set'", 'to': "orm['sp.ExtrasDetailModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_detail_participate_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'schedule': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'sp.feature': {
            'Meta': {'object_name': 'Feature'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.featurevalue': {
            'Meta': {'object_name': 'FeatureValue'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feature_value_set'", 'to': "orm['sp.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.list': {
            'Meta': {'object_name': 'List'},
            'collaboration': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': "orm['sp.UserCollaborationDetail']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'list_set'", 'null': 'True', 'to': "orm['sp.Project']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'sp.mediafeature': {
            'Meta': {'object_name': 'MediaFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.mediafeaturevalue': {
            'Meta': {'object_name': 'MediaFeatureValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_feature_value_set'", 'to': "orm['sp.MediaFeature']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'sp.model': {
            'Meta': {'object_name': 'Model'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'cant_casting': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'cant_extra': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name_complete': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_set'", 'null': 'True', 'to': "orm['sp.Country']"}),
            'number_doc': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True'}),
            'phone_fixed': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'phone_mobil': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_doc': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'sp.modelfeaturedetail': {
            'Meta': {'object_name': 'ModelFeatureDetail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'feature_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_feature_detail_set'", 'to': "orm['sp.FeatureValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_feature_detail_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'sp.modelhascommercial': {
            'Meta': {'object_name': 'ModelHasCommercial'},
            'commercial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Commercial']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model_has_commercial_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'sp.pauta': {
            'Meta': {'object_name': 'Pauta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pauta_set'", 'to': "orm['sp.Project']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
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
            'realized': ('django.db.models.fields.DateField', [], {'null': 'True'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'photo_casting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_detail_model_set'", 'to': "orm['sp.PhotoCasting']"}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sp.photocastingdetailparticipate': {
            'Meta': {'object_name': 'PhotoCastingDetailParticipate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_detail_participate_set'", 'to': "orm['sp.PhotoCastingDetailModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_casting_detail_participate_set'", 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sp.picturedetailfeature': {
            'Meta': {'object_name': 'PictureDetailFeature'},
            'feature_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'picture_detail_feature_set'", 'to': "orm['sp.MediaFeatureValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'picture_detail_feature_set'", 'to': u"orm['fileupload.Picture']"})
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_detail_model_set'", 'null': 'True', 'to': "orm['sp.Model']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'representation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representation_detail_model_set'", 'to': "orm['sp.Representation']"}),
            'schedule': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'sp.studio': {
            'Meta': {'object_name': 'Studio'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.support': {
            'Meta': {'object_name': 'Support'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'sp.typecasting': {
            'Meta': {'object_name': 'TypeCasting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typeevent': {
            'Meta': {'object_name': 'TypeEvent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.typephotocasting': {
            'Meta': {'object_name': 'TypePhotoCasting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.usephotos': {
            'Meta': {'object_name': 'UsePhotos'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'sp.usercollaborationdetail': {
            'Meta': {'object_name': 'UserCollaborationDetail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sp.List']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'sp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'cod_emp': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sp']