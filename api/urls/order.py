from django.urls import path

from api.views.order import OrderCreateAPIView, SplitBillAPIView, UpdateCustomerOrder, CompleteOrderDetailAPIView, SeenAPIView

urlpatterns = [
    path('create-order/', OrderCreateAPIView.as_view(), name='create-order'),
    path('split-order/', SplitBillAPIView.as_view(), name='split-order'),
    path('update-customer-order', UpdateCustomerOrder.as_view(), name='update-customer-order'),
    path('complete-order/', CompleteOrderDetailAPIView.as_view(), name='complete-done'),
    path('seen-order/', SeenAPIView.as_view(), name='seen-orderdetail')
]

from api.views.order import TestFutureOrder
urlpatterns += [
    path('test-futureorder/', TestFutureOrder.as_view(), name='test-future' )
]