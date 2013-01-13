from __future__ import with_statement
from os import path
import os
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
       

def configure_platform(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.configure_platform()

def install_app(deployment):

    knife_command = "knife bootstrap"
    for instance in deployment.instances.all():
        knife_command += " %s" % instance.dns

    knife_command += " -i %s" % deployment.private_key.key.path
    knife_command += " -r 'role[%s]'" % deployment.role.role_name
    knife_command += " -x %s" % deployment.username
    knife_command += " --sudo"
    chef_dir = os.path.dirname(deployment.role.path_to_knife)
    return knife_command
       
def pre_delete_cleanup(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)
        config.terminate_instances()
      
      
