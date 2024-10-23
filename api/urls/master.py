from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

from ..views.master import CustomTokenObtainPairView, CustomerAPI, TerminalUpdateView, MasterBillDetailView, MasterBillBranch

router = routers.DefaultRouter()

router.register("customer", CustomerAPI)

urlpatterns = [
    path("master-login/", CustomTokenObtainPairView.as_view(), name="master-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="master-token_refresh"),
    
    path("master-terminal-update/", TerminalUpdateView.as_view(), name="master-terminal-update"),
    
    path('master-bill-endday/', MasterBillDetailView.as_view(), name='bill-detail'),
    path('master-bill-branch/', MasterBillBranch.as_view(), name='bill-silverplatter'),

] + router.urls
