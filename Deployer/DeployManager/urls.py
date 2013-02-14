from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('DeployManager.views',
    # Examples:
    # url(r'^$', 'AppValveDeploy.views.home', name='home'),
    # url(r'^AppValveDeploy/', include('AppValveDeploy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stream/', 'stream_response'),
    url(r'^install_app/(?P<deployment_id>\w+)', 'install_app'),
    url(r'^reinstall_app/(?P<deployment_id>\w+)', 'reinstall_app'),
)
