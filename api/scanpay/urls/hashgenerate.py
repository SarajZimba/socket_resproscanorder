from django.urls import path

from api.scanpay.views.hashgenerate import HashAPIView, GiveTableOutletHashAPIView, ClearHashValue
urlpatterns = [
    path('scanpay/create-hash/', HashAPIView.as_view(), name='create-hash'),
    path('scanpay/get-outlettable-hash/<str:hashvalue>', GiveTableOutletHashAPIView.as_view(), name='get-outlettable-hash'),
    path('scanpay/clear-hash/<str:hashvalue>', ClearHashValue.as_view(), name='clear-hash'),
    ]
