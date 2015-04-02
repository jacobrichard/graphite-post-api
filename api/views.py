from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sites.models import RequestSite
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError
)
from graphite.api.decorators import logged_in_or_basicauth
from socket import socket


class API(View):
    @method_decorator(logged_in_or_basicauth())
    def post(self, request):
        if (not request.META.get('HTTP_API_KEY') == request.user.profile.api_key
                or not request.user.profile.api_user):
            return HttpResponse('Unauthorized', status=401)
        try:
            sock = socket()
            sock.connect((settings.API_CARBON_HOST,
                          settings.API_CARBON_PORT))
            sock.sendall(request.raw_post_data + '\n')
            sock.close()
            return HttpResponse('OK')
        except socket.error, (value, message):
            return HttpResponseServerError("Could not open socket: " +
                                           message)
        finally:
            if sock:
                sock.close()
