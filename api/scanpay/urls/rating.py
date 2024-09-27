from django.urls import path

from api.scanpay.views.rating import RatingCreateAPIView

urlpatterns = [
    path('scanpay/create-rating/', RatingCreateAPIView.as_view(), name='create-rating'),
] 