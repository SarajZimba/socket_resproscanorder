from django.urls import path
from api.views.recipie import RecipieAPIView

urlpatterns = [
    # Your other URL patterns
    path('recipie-item/<int:id>/', RecipieAPIView.as_view(), name='recipie-item'),

]