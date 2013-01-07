from __future__ import with_statement
from os import path
from fabric.api import local, settings, abort
from fabric.api import *

#from DeployManager import settings
#from DeployManager.models import *

from AWSUtils import EC2Config



def fresh_deploy(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.bootstrap()

#    with lcd(deployment.role.path_to_knife):

def launch_instance(deployment):

 
    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.launch_instance()
       

def configure_platform(deployment):

    if deployment.service == "ec2":
        config = EC2Config(deployment)

    config.configure_platform()

