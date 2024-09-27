from discounts.models import discountflag, tbl_discounts
from rest_framework import serializers

class TimedDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = discountflag
        fields = ['id', 'discount', 'dayofweek', 'start_time', 'end_time', 'state']

from rest_framework import serializers

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_discounts
        fields = ['name', 'type', 'value']
