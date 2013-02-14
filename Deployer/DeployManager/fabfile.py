from __future__ import with_statement
from os import path
import os
import imp
from fabric.api import local, settings, abort
from fabric.api import *
from celery import task
#from DeployManager import settings
#from DeployManager.models import *

from AWSUtils import EC2Config



def fresh_deploy(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.bootstrap()

#    with lcd(deployment.role.path_to_knife):

@task
def launch_instance(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.launch_instance()

@task
def reinstall_app(deployment):

    print "XXFabfile: " + deployment.fabfile.name
    from fabric.context_managers import settings
    deploy_fab = imp.load_source('__main__', deployment.fabfile.name)
    hosts = ["%s@%s" % (deployment.username, instance.dns) for instance in deployment.instances.all()]
    for host in hosts:
        with settings(host_string=host, key_filename=deployment.private_key.key.name):
            deploy_fab.deploy()

def configure_platform(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.configure_platform()

@task
def install_app(deployment):

    knife_command = "knife bootstrap"
    for instance in deployment.instances.all():
        knife_command += " %s" % instance.dns

    knife_command += " -i %s" % deployment.private_key.key.path
    knife_command += " -r 'role[%s]'" % deployment.role.role_name
    knife_command += " -x %s" % deployment.username
    knife_command += " --sudo"
    chef_dir = os.path.dirname(deployment.role.path_to_knife)
    with lcd(chef_dir):
        local(knife_command)
    return knife_command
       
def pre_delete_cleanup(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)
        config.terminate_instances()
      
      
