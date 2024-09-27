from django.urls import path
from api.scanpay.views.customer import CustomerNormalRegister, CustomerNormalLoginView, CustomerGuestLoginCreate, CustomerGoogleLoginView, CustomerGoogleRegister, CustomerDetailsAPIView,CustomerAddDetailsAPIView

urlpatterns = [
    path("scanpay/customer-register/", CustomerNormalRegister.as_view(), name="customer-register"),
    path("scanpay/customer-normal-login/", CustomerNormalLoginView.as_view(), name="customer-normal-login"),

]
urlpatterns += [
    path("scanpay/customer-googleregister/", CustomerGoogleRegister.as_view(), name="customer-googleregister"),
    path("scanpay/customer-google-login/", CustomerGoogleLoginView.as_view(), name="customer-google-login"),
]
urlpatterns += [
    path("scanpay/customer-guest-login/", CustomerGuestLoginCreate.as_view(), name="customer-normal-login"),

]

urlpatterns += [
    path("scanpay/customer-details/<int:id>", CustomerDetailsAPIView.as_view(), name="customer-details"),
    path("scanpay/add-dob-phone/<int:id>", CustomerAddDetailsAPIView.as_view(), name="add-customer-details"),

]

from api.scanpay.views.customer import CustomerOrderItemHistory, CustomerOrderHistoryDate, ReduceCustomerLoyaltyPoints
urlpatterns += [
    path("scanpay/reduce-customerloyaltypoints/<int:customer>", ReduceCustomerLoyaltyPoints.as_view(), name="reduce-customer-loyaltypoints"),
    path("scanpay/customer-orderitemhistory/<int:customer_id>", CustomerOrderItemHistory.as_view(), name="give-orderitem-history"),
    path("scanpay/customer-orderhistory-date/<int:customer_id>", CustomerOrderHistoryDate.as_view(), name="give-order-history-date"),

    # path("add-dob-phone/<int:id>", CustomerAddDetailsAPIView.as_view(), name="add-customer-details"),


]