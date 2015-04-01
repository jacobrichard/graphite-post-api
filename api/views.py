from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError
)
from graphite.api.decorators import logged_in_or_basicauth
from socket import socket


@logged_in_or_basicauth()
def sink(request):
    if not request.user.profile.api_user or not request.META.get('HTTP_API_KEY') == request.user.profile.api_key:
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        try:
            sock = socket()
            sock.connect((settings.API_CARBON_HOST,
                          settings.API_CARBON_PORT))
            sock.sendall(request.raw_post_data + '\n')
            return HttpResponse('OK')
        except socket.error, (value, message):
            return HttpResponseServerError("Could not open socket: " +
                                           message)
        finally:
            if sock:
                sock.close()
    else:
        return HttpResponseNotAllowed("Not Implemented")
