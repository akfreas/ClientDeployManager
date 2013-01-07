from django.db.models.signals import pre_delete, pre_save, post_save, post_syncdb
from DeployManager.models import *
from django.contrib.auth import models as auth_app, get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import fabfile

def auto_create_superuser(*args, **kwargs):

    site = Site(domain="http://example.com", name="Example Site")
    site.save()


    user = User.objects.create_superuser("DeploymentAdmin", "a@a.com", "kasashi")
    user.save()

post_syncdb.connect(auto_create_superuser,
    sender=auth_app, dispatch_uid="django.contrib.auth.management.create_superuser")

def post_save_deployment(sender, instance, signal, *args, **kwargs):

    import fabfile
    if instance.status_flags.configured != True:

        fabfile.configure_platform(instance)

    if instance.status_flags.instance_launched != True:

        fabfile.launch_instance(instance)

post_save.connect(post_save_deployment, sender=Deployment)

