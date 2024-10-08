from django.urls import path

from api.views.test_socket import TestSocket

urlpatterns = [
    path('test-socket/', TestSocket.as_view(), name='test-socket')

    # Add other URL patterns as needed
]