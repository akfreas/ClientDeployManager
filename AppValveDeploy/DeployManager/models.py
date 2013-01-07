from django.db import models 
from DeployManager import settings
from bitfield import BitField


deployment_services = (
        ("ec2", "Amazon EC2"),
        ("rackspace", "RackSpace"),
        ("private", "Privately Hosted"),
        )
role_names = (
        ("appvalve-webapp", "AppValve Webapp"),
        )

authorized_services = (
        ("tcp", "TCP"), 
        ("udp", "UDP"),
        )

ec2_instance_types = (
        ("t1.micro", "Micro"),
        ("s1.small", "Small"),
        )

class Client(models.Model):

    def __unicode__(self):
        return self.contact_name

    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    client_since = models.DateField()
   

class Deployment(models.Model):

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Deployment, self).save(*args, **kwargs)
        else:
            super(Deployment, self).save(*args, **kwargs)


    client = models.ForeignKey('Client')
    date_launched = models.DateTimeField(blank=True, null=True)
    service = models.CharField(choices=deployment_services, max_length=200)
    current_app_version = models.CharField(max_length=200)
    app_location = models.CharField(max_length=200)
    private_key = models.ForeignKey('KeyPair', blank=True, null=True)
    role = models.ForeignKey('ChefRole')
    aws_secret_key = models.CharField(max_length=200, blank=True, null=True)
    aws_access_key_id = models.CharField(max_length=200, blank=True, null=True)
    aws_security_group_name = models.CharField(max_length=200, blank=True, null=True)
    ec2_instance_type = models.CharField(choices=ec2_instance_types, default="ec2", max_length=200)
    ec2_security_groups = models.ManyToManyField('Ec2SecurityGroup')
    ec2_ami = models.CharField(max_length=200)
    instances = models.ManyToManyField("Instance")
    status_flags = BitField(flags=(
                        'configured',
                        'instance_launched',)) ## TODO Perhaps this field shoudn't be called 'configured' but 'platform configured'


class Instance(models.Model):

    dns = models.CharField(max_length=200)
    instance_id = models.CharField(max_length=200)

class ChefRole(models.Model):

    def __unicode__(self):
        return self.role_name

    path_to_knife = models.FilePathField(path="/Users/akfreas/chef", match="knife\.rb", recursive=True)
    role_name = models.CharField(max_length=200)

class Ec2SecurityGroup(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    allowed_ports = models.ManyToManyField('Ec2SecurityGroupPort')

class Ec2SecurityGroupPort(models.Model):

    def __unicode__(self):
        return "%s (%s)" % (self.port_number, self.description)

    port_number = models.IntegerField()
    service = models.CharField(choices=authorized_services, max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)

class KeyPair(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    key = models.FileField(upload_to=settings.PRIVATE_KEY_ROOT)

