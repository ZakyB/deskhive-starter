"""Teaching-only, read-only XML-RPC gateway.

XML-RPC uses HTTP POST even for reads, so CSRF is exempted for this public
*read-only* classroom demonstration. Never expose this gateway on the
public Internet without authentication, TLS, rate limits and hardening.
"""
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from xmlrpc.server import SimpleXMLRPCDispatcher
from .xmlrpc_api import get_space_availability, list_available_spaces

@csrf_exempt
def xmlrpc_gateway(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if len(request.body) > 65536:
        return HttpResponse('XML-RPC request too large', status=413)
    dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding='utf-8')
    dispatcher.register_function(list_available_spaces, 'list_available_spaces')
    dispatcher.register_function(get_space_availability, 'get_space_availability')
    reply = dispatcher._marshaled_dispatch(request.body)
    return HttpResponse(reply, content_type='text/xml; charset=utf-8')
