from django.contrib import admin
from DeployManager.models import *

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

class ClientAdmin(admin.ModelAdmin):

    list_display = ('contact_name', 'contact_email', 'client_since')

admin.site.register(Client, ClientAdmin)

class DeploymentAdmin(admin.ModelAdmin):

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    list_display = ('date_launched', 'service', 'current_app_version')
    readonly_fields = ('instances', 'date_launched',)


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

