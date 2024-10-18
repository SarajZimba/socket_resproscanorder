from rest_framework import serializers
from product.models import tblModifications

class ModificatinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblModifications
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]