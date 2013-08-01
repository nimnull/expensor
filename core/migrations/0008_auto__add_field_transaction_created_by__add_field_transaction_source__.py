# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Transaction.created_by'
        db.add_column(u'core_transaction', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Transaction.source'
        db.add_column(u'core_transaction', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Account']),
                      keep_default=False)

        # Adding field 'Transaction.category'
        db.add_column(u'core_transaction', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.ExpenseCategory']),
                      keep_default=False)

        # Adding field 'Transaction.ratio'
        db.add_column(u'core_transaction', 'ratio',
                      self.gf('django.db.models.fields.FloatField')(default=1),
                      keep_default=False)

        # Adding field 'Transaction.amount_src'
        db.add_column(u'core_transaction', 'amount_src',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Transaction.bill_date'
        db.add_column(u'core_transaction', 'bill_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Transaction.created_at'
        db.add_column(u'core_transaction', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2013, 8, 1, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Transaction.dst_ct'
        db.add_column(u'core_transaction', 'dst_ct',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'Transaction.dst_id'
        db.add_column(u'core_transaction', 'dst_id',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Transaction.created_by'
        db.delete_column(u'core_transaction', 'created_by_id')

        # Deleting field 'Transaction.source'
        db.delete_column(u'core_transaction', 'source_id')

        # Deleting field 'Transaction.category'
        db.delete_column(u'core_transaction', 'category_id')

        # Deleting field 'Transaction.ratio'
        db.delete_column(u'core_transaction', 'ratio')

        # Deleting field 'Transaction.sr_amount'
        db.delete_column(u'core_transaction', 'amount_srс')

        # Deleting field 'Transaction.bill_date'
        db.delete_column(u'core_transaction', 'bill_date')

        # Deleting field 'Transaction.created_at'
        db.delete_column(u'core_transaction', 'created_at')

        # Deleting field 'Transaction.dst_ct'
        db.delete_column(u'core_transaction', 'dst_ct_id')

        # Deleting field 'Transaction.dst_id'
        db.delete_column(u'core_transaction', 'dst_id')


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
        u'core.account': {
            'Meta': {'object_name': 'Account'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.action': {
            'Meta': {'object_name': 'Action'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.currency': {
            'Meta': {'object_name': 'Currency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ratio': ('django.db.models.fields.FloatField', [], {'default': '1'})
        },
        u'core.expensecategory': {
            'Meta': {'object_name': 'ExpenseCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'works_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'})
        },
        u'core.salary': {
            'Meta': {'ordering': "('-active_from',)", 'object_name': 'Salary'},
            'active_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'salaries'", 'to': u"orm['core.Person']"})
        },
        u'core.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'bill_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ExpenseCategory']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'direction': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'dst_ct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'dst_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ratio': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']"}),
            'amount_src': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['core']
