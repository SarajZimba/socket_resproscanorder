from rest_framework import serializers
from product.models import ProductRecipie
from menu.models import MediaFile
from api.scanpay.serializers.menu import MediaFileSerializer

class RecipieSerializer(serializers.ModelSerializer):
    # instruction = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    #  = serializers.SerializerMethodField()
    imageList= serializers.SerializerMethodField()
    avg_prep_time = serializers.SerializerMethodField()
    class Meta:
        model = ProductRecipie

        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
        ]
    def get_imageList(self, obj):
        media_files = MediaFile.objects.filter(product__resproproduct=obj.product)
        return MediaFileSerializer(media_files, many=True).data
    
    def get_name(self, obj):
        return obj.product.title
    
    def get_unit(self, obj):
        return obj.product.unit
    
    def get_avg_prep_time(self, obj):
        return obj.product.average_prep_time