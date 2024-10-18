from django.urls import path
from api.views.modifications import ModificationAPIView

urlpatterns = [
    path('modifications/<int:id>', ModificationAPIView.as_view(), name='get-modifications' )
]