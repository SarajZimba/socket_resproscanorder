from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.scanpay.serializers.order import OrderDetailsSerializer,OrderSerializer, CustomOrderWithOrderDetailsSerializer
from django.db import transaction
from order.models import ScanPayOrder, ScanPayOrderDetails, BillRequest
from django.utils import timezone
import pytz
from rest_framework.permissions import AllowAny
from django.db.models import Q
from order.utils import send_delivery_notification
from menu.models import Menu
from order.utils import send_order_notification
from menu.models import Organization



class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None, *args, **kwargs):
        desired_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime = timezone.now().astimezone(desired_timezone)

        # Format the datetime as a string
        current_time_str = current_datetime.strftime('%I:%M %p')
        current_date_str = current_datetime.strftime('%Y-%m-%d')
        data = request.data
        data['state'] = "Pending"
        data['start_time'] = current_time_str
        data['date'] = current_date_str
        table_no = request.data['table_no']
        outlet_name = request.data['outlet']
        # order_not_completed_in_table = Order.objects.filter(
        #     Q(table_no=table_no) & ~Q(state="Completed") &Q(outlet=outlet_name)
        # ).order_by('id')
        
        order_not_completed_in_table = ScanPayOrder.objects.filter(
            Q(table_no=table_no) & ~Q(state="Completed") &  ~Q(state="Cancelled") &Q(outlet=outlet_name)& Q(status=True)
        ).order_by('id')

        if order_not_completed_in_table.exists():
            if order_not_completed_in_table.last().state == "Pending":
                order_details_data = request.data.get('order_details', [])

                for order_detail_data in order_details_data:
                    order_detail_data['order'] = order_not_completed_in_table.last().id
                order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
                if order_details_serializer.is_valid():
                    order_details_serializer.save()

                    # send_delivery_notification(outlet_name, table_no)
                send_order_notification(order_not_completed_in_table.last(), "Pending")
                    
                return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
                
                # else:
                #     # order.delete()
                #     return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            elif order_not_completed_in_table.last().state == "Accepted":             
                data['outlet_order'] = order_not_completed_in_table.last().outlet_order
                order_serializer = OrderSerializer(data=data)
                if order_serializer.is_valid():
                    order = order_serializer.save()
                    order_details_data = request.data.get('order_details', [])

                    for order_detail_data in order_details_data:
                        order_detail_data['order'] = order.id
                    order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
                    if order_details_serializer.is_valid():
                        order_details_serializer.save()
                    send_order_notification(order, "Accepted")

                    return Response(order_serializer.data, status=status.HTTP_201_CREATED)
                    
                    # else:
                    #     order.delete()
                    #     return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            order_serializer = OrderSerializer(data=data)
            if order_serializer.is_valid():
                order = order_serializer.save()
                order_details_data = request.data.get('order_details', [])

                for order_detail_data in order_details_data:
                    order_detail_data['order'] = order.id
                order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
                if order_details_serializer.is_valid():
                    order_details_serializer.save()
                send_order_notification(order, "Normal")

                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
                
                # else:
                #     order.delete()
                #     return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
        # return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        order_details_data = request.data

        for order_detail_data in order_details_data:
            order_id = order_detail_data.get('order')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order_details_serializer = OrderDetailsSerializer(data=request.data, many=True)
        
        if order_details_serializer.is_valid():
            with transaction.atomic():
                # Delete existing OrderDetails associated with the specified Order ID
                for order_detail_data in order_details_data:
                    ScanPayOrderDetails.objects.filter(order=order_detail_data['order']).delete()

                # Save new OrderDetails
                order_details_serializer.save()
        
            future_order = ScanPayOrder.objects.filter(order=order_detail_data['order']).first()
            print(f"future_order {future_order}")
            future_order_data = []
            if future_order:
                for order_detail_data in order_details_data:
                    ScanPayOrderDetails.objects.filter(order=future_order).delete()
                    print(f"This is the future order id {future_order.id}")
                    print()
                    order_detail_data['order'] = int(future_order.id)
                    future_order_data.append(order_detail_data)
                print(future_order_data)
                future_order_details_serializer = OrderDetailsSerializer(data=future_order_data, many=True)
                if future_order_details_serializer.is_valid():
                    future_order_details_serializer.save()
                else:
                    print("The data was not valid")

            return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class OrderListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')
        orders = ScanPayOrder.objects.filter(Q(outlet=outlet_name) & ~Q(state="Completed") & ~Q(state = "Cancelled") & Q(status = True))


        serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)

        return Response(serializer.data, 200)
    
# class OrderAcceptView(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request, *args, **kwargs):
#         order = kwargs.get('order')
#         outlet_order = kwargs.get('outlet_order')
#         desired_timezone = pytz.timezone('Asia/Kathmandu')
#         current_datetime = timezone.now().astimezone(desired_timezone)

#         # Format the datetime as a string
#         current_time_str = current_datetime.strftime('%I:%M %p')
#         # current_date_str = current_datetime.strftime('%Y-%m-%d')
#         order = ScanPayOrder.objects.get(id=order)
#         order.accepted_time = current_time_str
#         order.state = "Accepted"
#         order.outlet_order = outlet_order
#         order.save()
#         return Response("Order time recorded")

class OrderAcceptView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        order = kwargs.get('order')
        outlet_order = kwargs.get('outlet_order')
        desired_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime = timezone.now().astimezone(desired_timezone)

        first_scanpayorder = ScanPayOrder.objects.filter(outlet_order=outlet_order,status=True).order_by('id').first()
        order = ScanPayOrder.objects.get(id=order)

# check if order of that outlet order already exists in the scanpayorder if it exists then change the orderid of the ordetails or items to previous first order
        if first_scanpayorder:
            print("I was in accept API")
            orderdetails = order.scanpayorderdetails_set.filter(is_deleted=False, status=True)
            for orderdetail in orderdetails:
                orderdetail.order = first_scanpayorder
                orderdetail.save()
            order.delete()


        # for scanpayorder in scanpayorders:

        else:
            # Format the datetime as a string
            current_time_str = current_datetime.strftime('%I:%M %p')
            # current_date_str = current_datetime.strftime('%Y-%m-%d')
            order.accepted_time = current_time_str
            order.state = "Accepted"
            order.outlet_order = outlet_order
            order.save()
        return Response("Order time recorded")

from django.db.models import Sum
from decimal import Decimal
class OrderSessionTotal(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')
        table_no = kwargs.get('table_no')
        # print(f'oulet_order {outlet_order}')
        orders = ScanPayOrder.objects.filter(Q(outlet=outlet_name) & Q(table_no=table_no) & ~Q(state="Completed") & ~Q(state="Cancelled") & Q(status=True))
        # orders = Order.objects.filter(table_no=table_no)

        print(f'These are the orders {orders}')
        serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)

        total_inall_order_details = ScanPayOrderDetails.objects.filter(order__in=orders).aggregate(total=Sum('total'))
        totalquantity_inall_order_details = ScanPayOrderDetails.objects.filter(order__in=orders).aggregate(quantity=Sum('quantity'))
        print(totalquantity_inall_order_details)
        total_amount = total_inall_order_details['total'] if total_inall_order_details['total'] is not None else 0
        total_quantity = totalquantity_inall_order_details['quantity'] if totalquantity_inall_order_details['quantity'] is not None else 0
        total_items = ScanPayOrderDetails.objects.filter(order__in=orders).count()
        vat = total_amount * Decimal(0.13)

        if orders:
            print("orders", orders)
            first_order = orders.first()
            first_order_startdate = first_order.date
            startdate_str = first_order_startdate.strftime('%Y-%m-%d')
            startdatetime_str = startdate_str + " " + first_order.start_time
            customer_name = first_order.customer.name if first_order.customer else ""
        else:
            startdatetime_str = ""
            customer_name = ""

        grand_total = total_amount + vat

        order_dict = {

            "orders" : serializer.data,
            "sub_total" : round(total_amount, 2),
            "vat" : round(vat, 2),
            "grand_total": round(grand_total, 2),
            "total_quantity": total_quantity,
            "total_items": total_items,
            "start_datetime": startdatetime_str,
            "table_no": table_no,
            "customer_name" : customer_name


        }

        return Response(order_dict, 200)


class CancelOrderAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = ScanPayOrder.objects.get(pk=order_id)
            order.state = "Cancelled"
            order.status = False
            order.save()
            return Response("Order cancelled successfully", 200)
        except Exception as e:
            return Response("No order found having that id", 400)


# from api.serializers.order import RatingOrderDetailsSerializer
# class GiveItemsfromTable(APIView):
#     def get(self, request, *args, **kwargs):

#         outlet_name = kwargs.get('outlet_name')
#         table_no = kwargs.get('table_no')
#         # print(f'oulet_order {outlet_order}')
#         orders = Order.objects.filter(Q(outlet=outlet_name) & Q(table_no=table_no) & ~Q(state="Completed") & ~Q(state="Cancelled"))

#         orderdetails = OrderDetails.objects.filter(order__in=orders)

#         orderdetailserializer = RatingOrderDetailsSerializer(orderdetails, many=True)

#         return Response(orderdetailserializer.data, 200)

from collections import defaultdict
from api.scanpay.serializers.order import RatingOrderDetailsSerializer
class GiveItemsfromTable(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):

        outlet_name = kwargs.get('outlet_name')
        table_no = kwargs.get('table_no')
        # print(f'oulet_order {outlet_order}')
        orders = ScanPayOrder.objects.filter(Q(outlet=outlet_name) & Q(table_no=table_no) & ~Q(state="Completed") & ~Q(state="Cancelled")& Q(status=True))


        orderdetails = ScanPayOrderDetails.objects.filter(order__in=orders)

        item_groups = defaultdict(lambda: {
            'productId': None,
            'itemName': None,
            'total': 0,
            'image': None

        })
        
        for order_detail in orderdetails:
            item_key = order_detail.itemName  # Assuming this matches the field name in OrderDetails
            print(item_key)
            item_groups[item_key]['productId'] = Menu.objects.get(item_name = order_detail.itemName).id
            item_groups[item_key]['itemName'] = order_detail.itemName
            item_groups[item_key]['total'] += float(order_detail.total)  # Assuming total is a string
            item_groups[item_key]['image'] = Menu.objects.get(item_name = order_detail.itemName).thumbnail if Menu.objects.get(item_name = order_detail.itemName).thumbnail else None

        
        combined_items = []
        for key, value in item_groups.items():
            combined_items.append({
                'productId': value['productId'],
                'itemName': value['itemName'],
                'total': str(value['total']),  # Convert total back to string if needed
                'image': value['image'].url if value['image'] else None

            })


        return Response(combined_items, 200)



from django.db.models import Q
from rating.models import tblRatings
class ReviewPending(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        table_no = kwargs.get('table_no')
        outlet = kwargs.get('outlet_name')
        flag = True
        order_queryset = ScanPayOrder.objects.filter(Q(table_no=table_no) & Q(outlet=outlet) & (Q(state='Pending') | Q(state='Cooked') | Q(state='Accepted'))& Q(status=True))
        if order_queryset.exists():
            order = order_queryset.first()
            if BillRequest.objects.filter(order=order).exists():
                if tblRatings.objects.filter(order = order).exists():
                    flag=False
                else:
                    flag = True
            else:
                flag = False
        else:
            flag=False
        flag_data = {
            "flag":flag
        }
        return Response(flag_data, 200)
        

class CompleteOrderAPIView(APIView):
    permission_classes = [AllowAny]
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order_details_data = request.data
        try:
            order = ScanPayOrder.objects.get(pk=order_id)
            customer = order.customer
            order.state = "Completed"
            order.save()
            total_of_ordersession = 0.0
            for order_detail_data in order_details_data:
                order_detail_data['order'] = order.id
                quantity = order_detail_data.pop('qty', None)
                itemName = order_detail_data.pop('title', None)
                total = order_detail_data.pop('amount', None)
                order_detail_data['quantity'] = quantity
                order_detail_data['itemName'] = itemName
                order_detail_data['total'] = total
                total_of_ordersession += order_detail_data['total']

            try:
                ScanPayOrderDetails.objects.filter(order=order_detail_data['order']).delete()
            except Exception as e:
                return Response("Error occured during deleting order", 400)

            order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
            if order_details_serializer.is_valid():
                order_details_serializer.save()
            else:
                return Response(order_details_serializer.errors, status=400)
            if customer:
                loyaltyPercentage = Organization.objects.first().loyalty_percentage
                loyalty_points = (loyaltyPercentage/100) * total_of_ordersession
                current_customerLoyaltypoints = customer.loyalty_points 
                customer.loyalty_points = round(current_customerLoyaltypoints + loyalty_points, 2)
                customer.save()
            return Response("Order completed successfully", 200)
        except Exception as e:
            return Response("No order found having that id", 400)
            
from organization.models import Table, Terminal, Branch   
def get_terminal_obj(branch, table):
    terminals = Terminal.objects.filter(branch=branch, is_deleted=False, status=True)

    print(f'{terminals}')
    for terminal in terminals:
        if Table.objects.filter(terminal=terminal, table_number=table).exists():
            return terminal
        
    # If no matching table was found, print a message and return None
    print(f"Following table number {table} is not associated with any terminal of the branch {branch}")
    return None


class CheckOrderCode(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        code = data['code']
        branch = data['branch']
        table = int(data['table'])


        branch_obj = Branch.objects.filter(branch_code=branch, status=True, is_deleted=False).first()

        terminal = get_terminal_obj(branch_obj, table)

        print(f'terminal {terminal}')

        table_obj = Table.objects.filter(terminal=terminal, table_number=table, status=True, is_deleted=False).first()

        if table_obj.is_occupied == True:
            if ScanPayOrder.objects.filter(table_no=table, outlet=branch, code=code, status=True).exists():
                return Response({'can_enter':'True'},200)
            
            else:
                return Response({'can_enter':'False'}, 200)
        else:
            return Response({'can_enter':'True'}, 200)
        

