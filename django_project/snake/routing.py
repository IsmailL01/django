from django.urls import re_path
from .consumers import SnakeGameConsumer

websocket_urlpatterns = [
    re_path(r'ws/snake/$', SnakeGameConsumer.as_asgi()),  
]
