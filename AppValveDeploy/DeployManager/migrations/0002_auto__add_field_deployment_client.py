# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Deployment.client'
        db.add_column(u'DeployManager_deployment', 'client',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['DeployManager.Client']),
                      keep_default=False)

        # Removing M2M table for field client on 'Deployment'
        db.delete_table('DeployManager_deployment_client')


    def backwards(self, orm):
        # Deleting field 'Deployment.client'
        db.delete_column(u'DeployManager_deployment', 'client_id')

        # Adding M2M table for field client on 'Deployment'
        db.create_table(u'DeployManager_deployment_client', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deployment', models.ForeignKey(orm[u'DeployManager.deployment'], null=False)),
            ('client', models.ForeignKey(orm[u'DeployManager.client'], null=False))
        ))
        db.create_unique(u'DeployManager_deployment_client', ['deployment_id', 'client_id'])


    models = {
        u'DeployManager.chefrole': {
            'Meta': {'object_name': 'ChefRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path_to_knife': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/akfreas/chef'", 'max_length': '100', 'recursive': 'True', 'match': "'knife\\\\.rb'"}),
            'role_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.client': {
            'Meta': {'object_name': 'Client'},
            'client_since': ('django.db.models.fields.DateField', [], {}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'DeployManager.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'app_location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'aws_access_key_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'aws_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'aws_security_group_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DeployManager.Client']"}),
            'current_app_version': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_launched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ec2_ami': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ec2_instance_type': ('django.db.models.fields.CharField', [], {'default': "'ec2'", 'max_length': '200'}),
            'ec2_security_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['DeployManager.Ec2SecurityGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['DeployManager.Instance']", 'symmetrical': 'False'}),
            'private_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DeployManager.KeyPair']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DeployManager.ChefRole']"}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.ec2securitygroup': {
            'Meta': {'object_name': 'Ec2SecurityGroup'},
            'allowed_ports': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['DeployManager.Ec2SecurityGroupPort']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.ec2securitygroupport': {
            'Meta': {'object_name': 'Ec2SecurityGroupPort'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port_number': ('django.db.models.fields.IntegerField', [], {}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.instance': {
            'Meta': {'object_name': 'Instance'},
            'dns': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.keypair': {
            'Meta': {'object_name': 'KeyPair'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['DeployManager']