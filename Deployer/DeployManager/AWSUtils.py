#!/usr/bin/env python
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError
from django.core.files import File
from tempfile import mkstemp, mkdtemp
from datetime import datetime
import os
from DeployManager.models import *
from django.db.models import F
import logging

logger = logging.getLogger("DeployManager.streaming.LogStreamer")

class EC2Config(object):

    """
    Right now, there isn't a way to log or print status of each of these
    config actions. What should be put into place is the use of a logging
    system that django can listen for and print messages accordingly (novel, I know).
    Right now, we'll just print to stdout.
    """

    def __init__(self, deployment, *args, **kwargs):
        
        self.deployment = deployment
        self.access_key = deployment.client.aws_access_key_id
        self.secret_key = deployment.client.aws_secret_key
        self.connection = EC2Connection(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

    def create_security_groups(self, security_group_list=None):

            
            if security_group_list is not None:
                groups = security_group_list
            else:
                groups = self.deployment.ec2_security_groups.all()

            print "Creating security groups for %s" % ", ".join([x.name for x in groups])
            for group in groups:
                try:
                    security_group = self.connection.create_security_group(group.name, group.description)
                    sec = lambda x: security_group.authorize(x.service, x.port_number, x.port_number, "0.0.0.0/0")

                    for port in group.allowed_ports.all():
                        sec(port)
                except EC2ResponseError as e:
                    print "Error creating security group:: " + e.error_message


    def create_key_pair(self):

        try:
            key_pair_name = "%s-%s" % (self.deployment.client.contact_name, self.deployment.id)
            key = self.connection.create_key_pair(key_pair_name)
            #temp_key_file, temp_key_path = mkstemp()
            temp_key_path = mkdtemp()
            key.save(temp_key_path)
            temp_key_path = "%s/%s.pem" % (temp_key_path, key_pair_name)

            key_file = File(open(temp_key_path))
            from DeployManager.models import KeyPair
            private_key = KeyPair(name=key_pair_name, key=key_file)
            private_key.save()
            os.chmod(private_key.key.path, 0600)
            self.deployment.private_key = private_key
            key_file.close()

        except EC2ResponseError as e:
            print e.error_message

    def launch_instance(self):


        """
        This method should be extended to support multiple instances,
        but for right now we probably don't need to support them though
        it should be a todo in the near future.
        """

        print "Getting image %s..." % self.deployment.ec2_ami
        image = self.connection.get_image(self.deployment.ec2_ami)
        security_groups = [x.name for x in self.deployment.ec2_security_groups.all()]
        print "Creating reservation for %s instance with private key: %s security groups %s" % (self.deployment.ec2_instance_type, self.deployment.private_key.name, ", ".join([x.name for x in self.deployment.ec2_security_groups.all()]))
        reservation = None
        try:
            reservation = image.run(key_name=self.deployment.private_key.name,
                                security_groups=security_groups, 
                                instance_type=self.deployment.ec2_instance_type)

        except EC2ResponseError as e:
            print "Error launching instance: " + e.error_message

        s = lambda y: list(set([x.update() for x in y.instances]))

        states = s(reservation)

        from DeployManager.models import Instance
        print "Waiting for instances to start..."

        while len(states) != 1 and states[0] !=  "pending": # block until all instances are running
            states = s(reservation)
            print states

        while 0 in map(lambda l: len(l), [x.dns_name for x in reservation.instances]):
            s(reservation)

        for instance in reservation.instances:

            model_instance = Instance(dns=instance.dns_name, instance_id=instance.id)
            model_instance.save()
            self.deployment.instances.add(model_instance)
        
        self.deployment.date_launched = datetime.now()
        self.deployment.status_flags.instance_launched = True
        self.deployment.save()

    def configure_platform(self):

        self.create_security_groups()
        self.create_key_pair()
        self.deployment.status_flags.configured = True
        self.deployment.save()

    def get_status(self):

        reservation = self.connection.get_all_instances(filters={'instance-id' : [instance.instance_id for instance in self.deployment.instances.all()]})
        if len(reservation) > 0:
            states = [{'id' : i.id, 'state' : i.state} for i in reservation[0].instances]
        else:
            states = [{'state' : "likely terminated"}]
        return states
        
    def terminate_instances(self):

        try:
            instance_ids = [d.instance_id for d in self.deployment.instances.all()]
            self.connection.terminate_instances(instance_ids)

        except EC2ResponseError as e:
            pass




    def create_machine(self):

        self.launch_instance()
    
    def bootstrap(self):

        self.configure_platform()
        self.launch_instance()

