# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'DeployManager_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('client_since', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'DeployManager', ['Client'])

        # Adding model 'Deployment'
        db.create_table(u'DeployManager_deployment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_launched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('current_app_version', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('app_location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('private_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DeployManager.KeyPair'], null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DeployManager.ChefRole'])),
            ('aws_secret_key', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('aws_access_key_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('aws_security_group_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ec2_instance_type', self.gf('django.db.models.fields.CharField')(default='ec2', max_length=200)),
            ('ec2_ami', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'DeployManager', ['Deployment'])

        # Adding M2M table for field client on 'Deployment'
        db.create_table(u'DeployManager_deployment_client', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deployment', models.ForeignKey(orm[u'DeployManager.deployment'], null=False)),
            ('client', models.ForeignKey(orm[u'DeployManager.client'], null=False))
        ))
        db.create_unique(u'DeployManager_deployment_client', ['deployment_id', 'client_id'])

        # Adding M2M table for field ec2_security_groups on 'Deployment'
        db.create_table(u'DeployManager_deployment_ec2_security_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deployment', models.ForeignKey(orm[u'DeployManager.deployment'], null=False)),
            ('ec2securitygroup', models.ForeignKey(orm[u'DeployManager.ec2securitygroup'], null=False))
        ))
        db.create_unique(u'DeployManager_deployment_ec2_security_groups', ['deployment_id', 'ec2securitygroup_id'])

        # Adding M2M table for field instances on 'Deployment'
        db.create_table(u'DeployManager_deployment_instances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deployment', models.ForeignKey(orm[u'DeployManager.deployment'], null=False)),
            ('instance', models.ForeignKey(orm[u'DeployManager.instance'], null=False))
        ))
        db.create_unique(u'DeployManager_deployment_instances', ['deployment_id', 'instance_id'])

        # Adding model 'Instance'
        db.create_table(u'DeployManager_instance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dns', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('instance_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'DeployManager', ['Instance'])

        # Adding model 'ChefRole'
        db.create_table(u'DeployManager_chefrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path_to_knife', self.gf('django.db.models.fields.FilePathField')(path='/Users/akfreas/chef', max_length=100, recursive=True, match='knife\\.rb')),
            ('role_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'DeployManager', ['ChefRole'])

        # Adding model 'Ec2SecurityGroup'
        db.create_table(u'DeployManager_ec2securitygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'DeployManager', ['Ec2SecurityGroup'])

        # Adding M2M table for field allowed_ports on 'Ec2SecurityGroup'
        db.create_table(u'DeployManager_ec2securitygroup_allowed_ports', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ec2securitygroup', models.ForeignKey(orm[u'DeployManager.ec2securitygroup'], null=False)),
            ('ec2securitygroupport', models.ForeignKey(orm[u'DeployManager.ec2securitygroupport'], null=False))
        ))
        db.create_unique(u'DeployManager_ec2securitygroup_allowed_ports', ['ec2securitygroup_id', 'ec2securitygroupport_id'])

        # Adding model 'Ec2SecurityGroupPort'
        db.create_table(u'DeployManager_ec2securitygroupport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port_number', self.gf('django.db.models.fields.IntegerField')()),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'DeployManager', ['Ec2SecurityGroupPort'])

        # Adding model 'KeyPair'
        db.create_table(u'DeployManager_keypair', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('key', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'DeployManager', ['KeyPair'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'DeployManager_client')

        # Deleting model 'Deployment'
        db.delete_table(u'DeployManager_deployment')

        # Removing M2M table for field client on 'Deployment'
        db.delete_table('DeployManager_deployment_client')

        # Removing M2M table for field ec2_security_groups on 'Deployment'
        db.delete_table('DeployManager_deployment_ec2_security_groups')

        # Removing M2M table for field instances on 'Deployment'
        db.delete_table('DeployManager_deployment_instances')

        # Deleting model 'Instance'
        db.delete_table(u'DeployManager_instance')

        # Deleting model 'ChefRole'
        db.delete_table(u'DeployManager_chefrole')

        # Deleting model 'Ec2SecurityGroup'
        db.delete_table(u'DeployManager_ec2securitygroup')

        # Removing M2M table for field allowed_ports on 'Ec2SecurityGroup'
        db.delete_table('DeployManager_ec2securitygroup_allowed_ports')

        # Deleting model 'Ec2SecurityGroupPort'
        db.delete_table(u'DeployManager_ec2securitygroupport')

        # Deleting model 'KeyPair'
        db.delete_table(u'DeployManager_keypair')


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
            'client': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['DeployManager.Client']", 'symmetrical': 'False'}),
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