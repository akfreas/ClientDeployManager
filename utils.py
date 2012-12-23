#!/usr/bin/env python
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError


class AppValveEc2Config(object):

    def __init__(self, access_key_id, secret_access_key, *args, **kwargs):
        
        self.access_key = access_key_id
        self.secret_key = secret_access_key
        self.connection = EC2Connection(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    def create_security_group(self):

        try:
            security_group = self.connection.create_security_group("AppValve", "Security group for AppValve beta testing platform.")
            sec = lambda x: security_group.authorize("tcp", x, x, "0.0.0.0/0")
            sec("80")
            sec("22")
            sec("443")
            sec("3306")

        except EC2ResponseError as e:
            print e.error_message

    def create_key_pair(self, path):

        try:
            key = self.connection.create_key_pair("AppValveKey")
            key.save(path)
        except EC2ResponseError as e:
            print e.error_message



    

if __name__ == "__main__":
    a = AppValveEc2Config("AKIAID3IGSY26I4WW4JA", "gBC7DCp/IWSO9Etmrx1a2fsC/jy4jqFr2lk5vg46")
    a.create_security_group()
    a.create_key_pair(".")
