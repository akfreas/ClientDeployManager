from django.contrib import admin
from DeployManager.models import *

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from AWSUtils import EC2Config
import fabfile

from itertools import imap

class InstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Instance, InstanceAdmin)

class ClientAdmin(admin.ModelAdmin):

    list_display = ('contact_name', 'contact_email', 'client_since')

admin.site.register(Client, ClientAdmin)

class DeploymentAdmin(admin.ModelAdmin):

    def deployment_status(self, obj):

        status = ["%s instance %s" % (sum(imap(lambda t: t == state, [x['state'] for x in obj.status])), state) for state in set([n['state'] for n in obj.status])]

        status = ", ".join(status)

        return status

    def save_model(self, request, obj, form, change):
        if obj.service == "ec2":
            config = EC2Config(obj)
            config.create_security_groups(form.cleaned_data['ec2_security_groups'])
        super(DeploymentAdmin, self).save_model(request, obj, form, change)

    def knife_command(self, obj):
        return fabfile.install_app(obj)

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    list_display = ('date_launched', 'service', 'current_app_version', 'deployment_status')
    readonly_fields = ('instances', 'date_launched', 'knife_command')


admin.site.register(Deployment, DeploymentAdmin)

class ChefRoleAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChefRole, ChefRoleAdmin)

class KeyPairAdmin(admin.ModelAdmin):
    
    list_display = ('name',)

admin.site.register(KeyPair, KeyPairAdmin)

class Ec2SecurityGroupPortInline(admin.TabularInline):
    model = Ec2SecurityGroupPort

class Ec2SecurityGroupPortAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ec2SecurityGroupPort, Ec2SecurityGroupPortAdmin)

class Ec2SecurityGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

#    inlines = [Ec2SecurityGroupPortInline]

admin.site.register(Ec2SecurityGroup, Ec2SecurityGroupAdmin)

