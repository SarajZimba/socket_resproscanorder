from order.models import HashValue
from rest_framework import serializers

class HashValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashValue
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]