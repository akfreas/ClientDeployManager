from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect

from DeployManager.models import *
import fabfile
import time 
import logging

logger = logging.getLogger("DeployManager.streaming.LogStreamer")

def stream_response(request):
    resp = StreamingHttpResponse( stream_response_generator())
    return resp

def stream_response_generator():
    for x in range(1,11):
        yield "%s\n" % x  # Returns a chunk of the response to the browser
        time.sleep(1)

def reinstall_app(request, deployment_id):
    deployment = Deployment.objects.get(id=deployment_id)
    fabfile.reinstall_app.delay(deployment)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def install_app(request, deployment_id):

    deployment = Deployment.objects.get(id=deployment_id)
    fabfile.install_app.delay(deployment)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
