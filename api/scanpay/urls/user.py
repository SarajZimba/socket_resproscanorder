# In urls.py
from django.urls import path
from api.scanpay.views.user import UserLoginCreateAPIView

urlpatterns = [
    path('scanpay/userlogin/', UserLoginCreateAPIView.as_view(), name='userlogin-create'),
    # Other paths for your application
]
