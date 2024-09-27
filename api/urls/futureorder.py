from django.urls import path

from api.views.futureorder import OrderCreateAPIView, SplitBillAPIView, UpdateCustomerOrder,FutureOrderList, FutureOrderDetailsList,FutureOrderUpdateAPIView,FutureToNormalOrderUpdateAPIView,FutureToCompletedOrderUpdateAPIView,FutureToCancelledOrderUpdateAPIView
urlpatterns = [
    path('create-future-order/', OrderCreateAPIView.as_view(), name='create-future-order'),
    path('split-futureorder/', SplitBillAPIView.as_view(), name='split-future-order'),
    path('update-customer-order', UpdateCustomerOrder.as_view(), name='update-customer-future-order'),
    path('future-orders', FutureOrderList.as_view(), name='future-orderlists'), 
    path('future-orderdetails/<int:futureorder_id>', FutureOrderDetailsList.as_view(), name='future-orders'), 
    path('future-orders/<int:pk>/', FutureOrderUpdateAPIView.as_view(), name='future-order-update'),
    path('to-normalorders/<int:pk>/<int:normalorder>/', FutureToNormalOrderUpdateAPIView.as_view(), name='future-order-to-normalorder'),
    path('future-completed/<int:pk>/', FutureToCompletedOrderUpdateAPIView.as_view(), name='future-order-completed'),
    path('future-cancelled/<int:pk>/', FutureToCancelledOrderUpdateAPIView.as_view(), name='future-order-cancelled')


]