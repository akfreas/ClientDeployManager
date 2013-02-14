# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Ec2SecurityGroup.description'
        db.alter_column(u'DeployManager_ec2securitygroup', 'description', self.gf('django.db.models.fields.CharField')(default='Fill-in description.', max_length=200))
        # Deleting field 'Deployment.aws_security_group_name'
        db.delete_column(u'DeployManager_deployment', 'aws_security_group_name')

        # Adding field 'Deployment.username'
        db.add_column(u'DeployManager_deployment', 'username',
                      self.gf('django.db.models.fields.CharField')(default='ubuntu', max_length=200),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Ec2SecurityGroup.description'
        db.alter_column(u'DeployManager_ec2securitygroup', 'description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))
        # Adding field 'Deployment.aws_security_group_name'
        db.add_column(u'DeployManager_deployment', 'aws_security_group_name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Deployment.username'
        db.delete_column(u'DeployManager_deployment', 'username')


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
            'service': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status_flags': ('django.db.models.fields.BigIntegerField', [], {'default': 'None'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'DeployManager.ec2securitygroup': {
            'Meta': {'object_name': 'Ec2SecurityGroup'},
            'allowed_ports': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['DeployManager.Ec2SecurityGroupPort']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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