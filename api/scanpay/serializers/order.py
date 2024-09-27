from order.models import ScanPayOrder, ScanPayOrderDetails
from menu.models import Menu
from rest_framework import serializers
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanPayOrder
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def create(self, validated_data):
        return ScanPayOrder.objects.create(**validated_data)
    
class OrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScanPayOrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def create(self, validated_data):
        return ScanPayOrderDetails.objects.create(**validated_data)
        
        
class RatingOrderDetailsSerializer(serializers.ModelSerializer):
    productId = serializers.SerializerMethodField()
    class Meta:
        model = ScanPayOrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def create(self, validated_data):
        return ScanPayOrderDetails.objects.create(**validated_data)
    
    def get_productId(self, obj):
        menu_id = Menu.objects.get(item_name=obj.itemName).id
        return menu_id

from order.utils import get_productId
class CustomOrderDetailsSerializer(serializers.ModelSerializer):

    product_id = serializers.SerializerMethodField()
    menu_id = serializers.SerializerMethodField()

    class Meta:
        model = ScanPayOrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_product_id(self, obj):
        productId = get_productId(obj.itemName)
        return productId
    def get_menu_id(self, obj):
        menu_id = Menu.objects.get(item_name=obj.itemName).id
        return menu_id
from django.utils import timezone
import pytz   
from order.utils import get_terminal
class CustomOrderWithOrderDetailsSerializer(serializers.ModelSerializer):
    products = CustomOrderDetailsSerializer(source='scanpayorderdetails_set', many=True, read_only=True)
    updated_time = serializers.SerializerMethodField()

    terminal_no = serializers.SerializerMethodField()
    # bot = serializers.SerializerMethodField()
    # kot = serializers.SerializerMethodField()
    # tableNumber = serializers.SerializerMethodField()
    
    customer_name = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    loyalty_points = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField() 
    class Meta:
        model = ScanPayOrder
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    # def get_bot(self, obj):
    #     return int(obj.orderdetails_set.first().botID) if (obj.orderdetails_set.first() is not None and obj.orderdetails_set.first().botID is not None)else None
    
    # def get_kot(self, obj):
    #     return int(obj.orderdetails_set.first().kotID) if (obj.orderdetails_set.first() is not None and obj.orderdetails_set.first().kotID is not None) else None
    
    # def get_tableNumber(self, obj):
    #     return str(obj.table_no) if (obj.orderdetails_set.first() is not None and obj.table_no is not None) else None
    def get_updated_time(self, obj):
        local_tz = pytz.timezone('Asia/Kathmandu')
        return obj.scanpayorderdetails_set.order_by('id').last().created_at.astimezone(local_tz).strftime("%I:%M %p") if (obj.scanpayorderdetails_set.last() is not None) else None
    
    def get_terminal_no(slf, obj):
        from organization.models import Branch
        branch=Branch.objects.filter(branch_code=obj.outlet, is_deleted=False, status=True).first()
        terminal = get_terminal(branch, obj.table_no)

        return terminal
        
    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None
    
    def get_address(self, obj):
        return obj.customer.address if obj.customer else None
    
    def get_mobile_number(self, obj):
        return obj.customer.phone if obj.customer else None
    
    def get_loyalty_points(self, obj):
        return str(obj.customer.loyalty_points) if obj.customer else None
    
    def get_email(self, obj):
        return obj.customer.email if obj.customer else None
    
class NormalToScanPayOrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScanPayOrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def create(self, validated_data):
        return ScanPayOrderDetails.objects.create(**validated_data)
