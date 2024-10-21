from rest_framework import serializers
from bill.models import Bill, BillItem, BillPayment, BillItemVoid
from api.serializers.order import CustomOrderWithOrderDetailsSerializer
# from api.serializers.organization import PrinterSettingSerializer
from organization.models import Table_Layout, Table
from api.serializers.bill import BillItemVoidSerializerTerminalSwitch
from api.serializers.bill import MobilePaymentSummarySerializer
from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ObjectDoesNotExist

from bill.models import MobilePaymentSummary
class MobilePaymentSummarySerializerBill(ModelSerializer):
    mobileOptionId = serializers.SerializerMethodField()
    mobileOptionName = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    class Meta:
        model = MobilePaymentSummary
        fields = [
            "type",
            "value",
            "mobileOptionId",
            "mobileOptionName",
            "amount"
        ]
        
    def get_mobileOptionId(self, obj):
        return obj.type.id
        
    def get_mobileOptionName(self, obj):
        return obj.type.name
        
    def get_amount(self, obj):
        return obj.value


class TableLayoutSerializer(serializers.ModelSerializer):
    tableNo = serializers.SerializerMethodField()
    class Meta:
        model = Table_Layout
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
        ]     

    def get_tableNo(self, obj):
        return obj.table_id.table_number
        
class TableSerializer(serializers.ModelSerializer):
    tablelayouts = TableLayoutSerializer(source='table_layout', allow_null=True)
    class Meta:
        model = Table
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
        ]  


class BillItemSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    print_display = serializers.SerializerMethodField()
    class Meta:
        model = BillItem
        fields = [
            "product_quantity",
            "product",
            "rate",
            "amount",
            "kot_id",
            "bot_id",
            "type",
            "print_display"
        ]
        
    def get_type(self, obj):
        return obj.product.type.title
    
    def get_print_display(self, obj):
        return obj.product.print_display

class PaymentModeSerializer(serializers.ModelSerializer):
    saleId = serializers.SerializerMethodField()
    class Meta:
        model = BillPayment
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "bill"
        ]

    def get_saleId(self, obj):
        return obj.bill.order.sale_id if obj.bill.order else None
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['amount'] = round(float(data['amount']), 2) if data['amount'] else 0.0
        
        return data  

class BillSerializer(serializers.ModelSerializer):
    bill_items = BillItemSerializer(many=True, read_only=True)

    payment_split = PaymentModeSerializer(source='billpayment_set', many=True, read_only=True)
    
    mobile_payment = MobilePaymentSummarySerializerBill(source='mobilepaymentsummary_set', many=True, read_only=True)


    order = CustomOrderWithOrderDetailsSerializer()

    isCompleted = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    isVoid = serializers.SerializerMethodField()

    tableNo = serializers.SerializerMethodField()
    noOfGuest = serializers.SerializerMethodField()
    
    is_cancelled = serializers.SerializerMethodField()
    startdatetime = serializers.SerializerMethodField()
    server_id = serializers.SerializerMethodField()
    is_synced = serializers.SerializerMethodField()
    void_items = serializers.SerializerMethodField()
    order_type = serializers.SerializerMethodField()
    is_future = serializers.SerializerMethodField()
    
    
    transaction_date_time = serializers.SerializerMethodField()


    class Meta:
        model = Bill
        exclude = [
            "created_at",
            "updated_at",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "status"
        ]
        
    def get_transaction_date_time(self, obj):
        return str(obj.transaction_date_time).split('+')[0]
        
    def get_void_items(self, obj):
        # Check if the bill has an associated order
        if obj.order:
            # Get the related BillItemVoid instances for the order
            bill_item_voids = BillItemVoid.objects.filter(order=obj.order)
            # Serialize the related BillItemVoid instances
            serializer = BillItemVoidSerializerTerminalSwitch(instance=bill_item_voids, many=True)
            return serializer.data
        return None
        
    def get_is_cancelled(self, obj):
        return False if (obj.order is not None and obj.order.orderdetails_set.first() is not None) else True
        
    def get_is_synced(self, obj):
        return True 
    
    def get_startdatetime(self, obj):
        return obj.order.start_datetime if obj.order else None
    
    def get_server_id(self, obj):
        return obj.order.id if obj.order else None

    def get_isCompleted(self, obj):
        return obj.order.is_completed if obj.order else None
    
    def get_isSaved(self, obj):
        return obj.order.is_saved if obj.order else None
    
    def get_organization(self, obj):
        return obj.organization.org_name if obj.organization else None
    
    def get_isVoid(self, obj):
        return False if obj.status else True
    
    def get_tableNo(self, obj):
        return str(obj.order.table_no) if (obj.order and obj.order.table_no) else None 
    
    def get_noOfGuest(self, obj):
        return obj.order.no_of_guest if obj.order else None
        
    def get_order_type(self, obj):
        return obj.order.order_type if obj.order else None

    def get_is_future(self, obj):
        
        future_order = obj.order.futureorder_set.exists()  # Accessing the related FutureOrder instance
        # If 'future_order' is accessed without exception, it means a FutureOrder exists
        if future_order:
            is_future = True
        else:
            # If ObjectDoesNotExist exception is raised, no FutureOrder exists
            is_future = False
        return is_future
        # return True if obj.order.futureorder else False
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sub_total'] = round(float(data['sub_total']), 2)
        data['discount_amount'] = round(float(data['discount_amount']), 2)
        data['taxable_amount'] = round(float(data['taxable_amount']), 2)
        data['tax_amount'] = round(float(data['tax_amount']), 2)
        data['grand_total'] = round(float(data['grand_total']), 2)
        data['service_charge'] = round(float(data['service_charge']), 2)
        
        return data