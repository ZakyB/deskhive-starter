from django.urls import path
from .views import xmlrpc_gateway

urlpatterns = [path("availability/", xmlrpc_gateway, name="m7-availability-rpc")]
