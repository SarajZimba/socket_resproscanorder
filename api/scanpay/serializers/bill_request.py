
from order.models import BillRequest
from rest_framework import serializers


class BillRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillRequest
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]