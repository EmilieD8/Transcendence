from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'wss/socket-server/', consumers.GameConsumer.as_asgi()),
    re_path(r'wss/socket-server/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
]
