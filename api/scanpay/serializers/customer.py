from user.models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    total_points = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "loyalty_points"
        ]

    def get_total_points(self, obj):
        return obj.loyalty_points