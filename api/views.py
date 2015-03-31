from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.http import HttpResponseNotAllowed, HttpResponse
from socket import socket

def sink(request):
    if request.method == "POST":
        sock = socket()
        sock.connect((settings.API_CARBON_HOST, settings.API_CARBON_PORT))
        sock.sendall(request.raw_post_data + '\n')
        return HttpResponse('OK')
    else:
        return HttpResponseNotAllowed("Not Implemented") 
