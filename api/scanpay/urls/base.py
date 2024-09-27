from api.scanpay.urls.discount import urlpatterns as discount_urlpatterns
from api.scanpay.urls.menu import urlpatterns as menu_urlpatterns
from api.scanpay.urls.order import urlpatterns as order_urlpatterns
from api.scanpay.urls.rating import urlpatterns as rating_urlpatterns
from api.scanpay.urls.hashgenerate import urlpatterns as hashgenerate_urlpatterns
from api.scanpay.urls.bill_request import urlpatterns as billrequest_urlpatterns
from api.scanpay.urls.customer import urlpatterns as customer_urlpatterns
from api.scanpay.urls.user import urlpatterns as user_urlpatterns

scanpay_urlpatterns = (
    [] + discount_urlpatterns + menu_urlpatterns + order_urlpatterns + rating_urlpatterns + hashgenerate_urlpatterns + billrequest_urlpatterns + customer_urlpatterns + user_urlpatterns
)