# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Salary'
        db.create_table(u'core_salary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('active_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'core', ['Salary'])

        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('works_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding model 'Action'
        db.create_table(u'core_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['Action'])

        # Adding field 'Transaction.comment'
        db.add_column(u'core_transaction', 'comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Salary'
        db.delete_table(u'core_salary')

        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Deleting model 'Action'
        db.delete_table(u'core_action')

        # Deleting field 'Transaction.comment'
        db.delete_column(u'core_transaction', 'comment')


    models = {
        u'core.action': {
            'Meta': {'object_name': 'Action'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'works_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'core.salary': {
            'Meta': {'object_name': 'Salary'},
            'active_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"})
        },
        u'core.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['core']