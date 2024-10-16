# menu/routing.py
from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),  # Ensure this matches your request
    re_path(r'ws/bar/$', consumers.BarConsumer.as_asgi()),  # Ensure this matches your request
    re_path(r'ws/product/$', consumers.ProductConsumer.as_asgi()),  # Ensure this matches your request
]