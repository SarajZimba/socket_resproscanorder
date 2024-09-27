from rating.models import tblRatings, tblitemRatings
from rest_framework import serializers
class tblRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblRatings
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def create(self, validated_data):
        return tblRatings.objects.create(**validated_data)
    
class tblitemRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblitemRatings
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def create(self, validated_data):
        return tblitemRatings.objects.create(**validated_data)