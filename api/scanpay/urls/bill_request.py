from django.urls import path

from api.scanpay.views.bill_request import BillRequestAPIView, BillRequestListAPIView, BillRequestConfirmAPIView, BillRequestwithDiscountAPIView

urlpatterns = [
    path('scanpay/bill-request/<str:outlet>', BillRequestAPIView.as_view(), name='bill-request'),
    path('scanpay/bill-request-list/<str:outlet>', BillRequestListAPIView.as_view(), name='bill-request-list'),
    path('scanpay/accept-billrequest/<int:billrequest_id>/', BillRequestConfirmAPIView.as_view(), name='billrequest-accept'),
    path('scanpay/bill-request-with-discount/<int:order>', BillRequestwithDiscountAPIView.as_view(), name='bill-request'),

] 
