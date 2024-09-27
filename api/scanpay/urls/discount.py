from api.scanpay.views.discount import CreateTimedDiscountView, DiscountCreateView, DiscountList #, DiscountStatus
from django.urls import path

urlpatterns = [
    path('api/create-timed-discount/', CreateTimedDiscountView.as_view(), name='create_timed_discount'),
]

urlpatterns += [
    path('scanpay/sync-discount/', DiscountCreateView.as_view(), name='discount-create'),
    # path('discount-status/', DiscountStatus.as_view(), name='discount-status'),
    path('scanpay/discount-list/', DiscountList.as_view(), name='discount-list'),

]