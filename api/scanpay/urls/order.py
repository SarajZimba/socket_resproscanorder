from django.urls import path

from api.scanpay.views.order import OrderCreateAPIView, OrderListView, OrderAcceptView, CancelOrderAPIView, CompleteOrderAPIView

urlpatterns = [
    path('scanpay/create-order/', OrderCreateAPIView.as_view(), name='create-order'),
    path('scanpay/give-order/<str:outlet_name>', OrderListView.as_view(), name='give-order'),
    path('scanpay/accept-order/<int:order>/<int:outlet_order>/', OrderAcceptView.as_view(), name='record-accept-time'),
    path('scanpay/cancel-order/<int:order_id>/', CancelOrderAPIView.as_view(), name='cancel-order'),
    path('scanpay/complete-order/<int:order_id>/', CompleteOrderAPIView.as_view(), name='complete-order'),
] 

from api.scanpay.views.order import OrderSessionTotal
urlpatterns += [
    path('scanpay/order-session/<str:outlet_name>/<int:table_no>/', OrderSessionTotal.as_view(), name='order-session'),
] 

from api.scanpay.views.order import GiveItemsfromTable
urlpatterns += [
    path('scanpay/table-items/<str:outlet_name>/<int:table_no>/', GiveItemsfromTable.as_view(), name='table-items'),
] 

from api.scanpay.views.order import ReviewPending

urlpatterns += [
    path('scanpay/is-pending/<str:outlet_name>/<int:table_no>/',ReviewPending.as_view(), name='is-session-comleted'),
] 

from api.scanpay.views.order import CheckOrderCode

urlpatterns += [
    path('scanpay/can-enter/',CheckOrderCode.as_view(), name='is-same-customer'),
] 