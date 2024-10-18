from django.urls import path
from api.views.void import VoidBillAPIView

urlpatterns = [
    path("void-items", VoidBillAPIView.as_view(), name='void-items' )
]

from api.views.void import VoidOrderTrackerAPIView
urlpatterns += [
    path('void-ordertrackers/', VoidOrderTrackerAPIView.as_view(), name='void-ordertrackers'),
]