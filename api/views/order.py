from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.order import OrderDetailsSerializer,OrderSerializer, tblOrderTrackerSerializer
from api.serializers.futureorder import FutureOrderDetailsSerializer #This is different orderserializer for futureorder
from bill.models import Order, OrderDetails, FutureOrder, FutureOrderDetails, tblOrderTracker
from django.db import transaction
from organization.models import Terminal, Branch
from product.models import Product
from rest_framework.permissions import AllowAny
from decimal import Decimal
from order.utils import send_order_notification_socket, send_bar_order_notification_socket, check_and_insert_updated_item, send_createorder_notification_socket_kitchen, send_createorder_notification_socket_bar, send_updateorder_notification_socket_bar, send_updateorder_notification_socket_kitchen

from django.db.models import Q
class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            order_serializer = OrderSerializer(data=request.data)
            if order_serializer.is_valid():
                order = order_serializer.save()
                order_details_data = request.data.get('order_details', [])

                for order_detail_data in order_details_data:
                    order_detail_data['order'] = order.id
                order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
                if order_details_serializer.is_valid():
                    order_details_serializer.save()
                    # send_order_notification_socket(order)
                    # send_bar_order_notification_socket(order)


                    tblordertracker_serializer = tblOrderTrackerSerializer(data=order_details_data, many=True)
                    if tblordertracker_serializer.is_valid():
                        tblordertracker_serializer.save()

                    if order.tblordertracker_set.filter(~Q(kotID=None)).exists():
                        if not order.tblordertracker_set.filter(~Q(botID=None)).exists():
                            send_createorder_notification_socket_kitchen(order)
                    if order.tblordertracker_set.filter(~Q(botID=None)).exists():

                        if not order.tblordertracker_set.filter(~Q(kotID=None) ).exists():
                            send_createorder_notification_socket_bar(order)
                    if order.tblordertracker_set.filter(~Q(botID=None)).exists():

                        if  order.tblordertracker_set.filter(~Q(kotID=None) ).exists():
                            send_createorder_notification_socket_bar(order)
                            send_createorder_notification_socket_kitchen(order)
                    return Response(order_serializer.data, status=status.HTTP_201_CREATED)

                else:
                    order.delete()
                    return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)    
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
                check_and_insert_updated_item(request.data)
                for order_detail_data in order_details_data:
                    OrderDetails.objects.filter(order=order_detail_data['order']).delete()

                # Save new OrderDetails
                order_details_serializer.save()


        
            future_order = FutureOrder.objects.filter(order=order_detail_data['order']).order_by('id').first()
            print(f"future_order {future_order}")
            future_order_data = []
            if future_order:
                for order_detail_data in order_details_data:
                    FutureOrderDetails.objects.filter(order=future_order).delete()
                    print(f"This is the future order id {future_order.id}")
                    print()
                    order_detail_data['order'] = int(future_order.id)
                    future_order_data.append(order_detail_data)
                print(future_order_data)
                future_order_details_serializer = FutureOrderDetailsSerializer(data=future_order_data, many=True)
                if future_order_details_serializer.is_valid():
                    future_order_details_serializer.save()
                else:
                    print("The future data was not valid")
                    
            from order.models import ScanPayOrder, ScanPayOrderDetails
            from api.scanpay.serializers.order import NormalToScanPayOrderDetailsSerializer
            scanpay_orders = ScanPayOrder.objects.filter(outlet_order=order_detail_data['order'])
            print(f"scanpay_order {scanpay_orders}")
            print(f"scanpay orderdetails data before changing {order_details_data}")
            scanpay_order_data = []
            if scanpay_orders:
                print(f"In this {scanpay_orders}")
                for order in scanpay_orders:

                    prev_orderdetails = ScanPayOrderDetails.objects.filter(order=order)
                    for orderdetails in prev_orderdetails:
                        orderdetails.delete()
                scanpay_order = scanpay_orders.order_by('id').first()
                for order_detail_data in order_details_data:
                    print(f"This is the scanpay order id {scanpay_order.id}")
                    order_detail_data['order'] = int(scanpay_order.id)
                    quantity = order_detail_data.pop('product_quantity', None)
                    productId = order_detail_data.pop('product', None)
                    rate = order_detail_data.get('rate', None)
                    order_detail_data['itemName'] = Product.objects.get(pk=int(productId)).title
                    order_detail_data['quantity'] = quantity
                    order_detail_data['total'] = Decimal(rate) * Decimal(quantity)


                    scanpay_order_data.append(order_detail_data)
                print(f"scanpay orderdetails data after changing {scanpay_order_data}")
                scanpay_order_details_serializer = NormalToScanPayOrderDetailsSerializer(data=scanpay_order_data, many=True)
                if scanpay_order_details_serializer.is_valid():
                    scanpay_order_details_serializer.save()
                else:
                    print("The scanpay data was not valid")

            # send_updateorder_notification_socket_kitchen(Order.objects.get(pk=order_id))
            # send_updateorder_notification_socket_bar(Order.objects.get(pk=order_id))
            # if Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(kotID=None)).exists():
            #     if not Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(botID=None)).exists():
            #         send_updateorder_notification_socket_kitchen(Order.objects.get(pk=order_id))
            # if Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(botID=None)).exists():

            #     if not Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(kotID=None) ).exists():
            #         send_updateorder_notification_socket_bar(Order.objects.get(pk=order_id))
            # if Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(botID=None)).exists():

            #     if Order.objects.get(pk=order_id).tblordertracker_set.filter(~Q(kotID=None) ).exists():
            #         send_updateorder_notification_socket_bar(Order.objects.get(pk=order_id))
            #         send_updateorder_notification_socket_kitchen(Order.objects.get(pk=order_id))
            # send_order_notification_socket()
            # send_bar_order_notification_socket()
            return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # def patch(self, request, format=None):
    #     order_details_data = request.data

    #     for order_detail_data in order_details_data:
    #         order_id = order_detail_data.get('order')
    #         if not order_id:
    #             return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     order_details_serializer = OrderDetailsSerializer(data=request.data, many=True)
        
    #     if order_details_serializer.is_valid():
    #         with transaction.atomic():
    #             # Delete existing OrderDetails associated with the specified Order ID
    #             # for order_detail_data in order_details_data:
    #             #     OrderDetails.objects.filter(order=order_detail_data['order']).delete()

    #             # Save new OrderDetails
    #             order_details_serializer.save()
        
    #         future_order = FutureOrder.objects.filter(order=order_detail_data['order']).order_by('id').first()
    #         print(f"future_order {future_order}")
    #         future_order_data = []
    #         if future_order:
    #             for order_detail_data in order_details_data:
    #                 # FutureOrderDetails.objects.filter(order=future_order).delete()
    #                 print(f"This is the future order id {future_order.id}")
    #                 print()
    #                 order_detail_data['order'] = int(future_order.id)
    #                 future_order_data.append(order_detail_data)
    #             print(future_order_data)
    #             future_order_details_serializer = FutureOrderDetailsSerializer(data=future_order_data, many=True)
    #             if future_order_details_serializer.is_valid():
    #                 future_order_details_serializer.save()
    #             else:
    #                 print("The future data was not valid")
                    
    #         from order.models import ScanPayOrder, ScanPayOrderDetails
    #         from api.scanpay.serializers.order import NormalToScanPayOrderDetailsSerializer
    #         scanpay_orders = ScanPayOrder.objects.filter(outlet_order=order_detail_data['order'])
    #         print(f"scanpay_order {scanpay_orders}")
    #         print(f"scanpay orderdetails data before changing {order_details_data}")
    #         order_details_scanpay = Order.objects.get(pk=order_id).orderdetails_set.all()
    #         scanpay_order_data = []
    #         if scanpay_orders:
    #             print(f"In this {scanpay_orders}")
    #             for order in scanpay_orders:

    #                 prev_orderdetails = ScanPayOrderDetails.objects.filter(order=order)
    #                 for orderdetails in prev_orderdetails:
    #                     orderdetails.delete()
    #             scanpay_order = scanpay_orders.order_by('id').first()
    #             for order_detail_data in order_details_scanpay:
    #                 print(f"This is the scanpay order id {scanpay_order.id}")
    #                 # order_detail_data['order'] = int(scanpay_order.id)
    #                 scanpay_order_detail_data = {
    #                     "order" : int(scanpay_order.id)
    #                 }
    #                 quantity = order_detail_data.product_quantity
    #                 productId = order_detail_data.product.id
    #                 rate = order_detail_data.rate
    #                 scanpay_order_detail_data['itemName'] = Product.objects.get(pk=int(productId)).title
    #                 scanpay_order_detail_data['quantity'] = quantity
    #                 scanpay_order_detail_data['total'] = Decimal(rate) * Decimal(quantity)
    #                 scanpay_order_detail_data['modification'] = order_detail_data.modification
    #                 scanpay_order_detail_data['rate'] = order_detail_data.rate




    #                 scanpay_order_data.append(scanpay_order_detail_data)
    #             print(f"scanpay orderdetails data after changing {scanpay_order_data}")
    #             scanpay_order_details_serializer = NormalToScanPayOrderDetailsSerializer(data=scanpay_order_data, many=True)
    #             if scanpay_order_details_serializer.is_valid():
    #                 scanpay_order_details_serializer.save()
    #             else:
    #                 print("The scanpay data was not valid")

    #         # send_order_notification_socket(Order.objects.get(pk=order_id))
    #         # send_bar_order_notification_socket(Order.objects.get(pk=order_id))
    #         send_order_notification_socket()
    #         send_bar_order_notification_socket()
    #         return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
    #     else:
    #         return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class SplitBillAPIView(APIView):
    
    @transaction.atomic()
    def post(self, request, format=None):
        try:
            data = request.data
            splitted_order_id = data['splitted_order_id']
            remaining_order = data.get("remaining_orders", [])
            split_order = data.get("split_order", {})

            # Delete the original orderdetails
            original_order = Order.objects.get(id=splitted_order_id)
            original_order_details = OrderDetails.objects.filter(order=splitted_order_id)
            original_order_details.delete()

            for order_detail_data in remaining_order:
                order_detail_data.pop("order")
                product_id = order_detail_data.pop("product")
                product = Product.objects.get(pk=product_id)
                order_detail_data["product"] = product

                OrderDetails.objects.create(order=original_order, **order_detail_data)



            branch_id = split_order.pop("branch")
            branch = Branch.objects.get(pk=branch_id)
            
            terminal_id = split_order.pop("terminal_no")
            terminal = Terminal.objects.get(terminal_no=terminal_id, branch=branch, is_deleted=False, status=True)

            # Create order with related objects
            split_order["terminal"] = terminal   
            split_order["branch"] = branch
            split_order["terminal_no"] = terminal_id

            order_details_data = split_order.pop("order_details", [])

            order = Order.objects.create(**split_order)

    
            for order_detail_data in order_details_data:
                order_detail_data.pop("order")
                product_id = order_detail_data.pop("product")
                product = Product.objects.get(pk=product_id)
                order_detail_data["product"] = product

                OrderDetails.objects.create(order=order, **order_detail_data)

            details = {
                        "order_id": order.id,
                        "sale_id": order.sale_id,
                        "is_saved":order.is_saved
                    }
            return Response(details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
from user.models import Customer
class UpdateCustomerOrder(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        customer = data['customer']
        order = data['order']
        try:

            order_obj = Order.objects.get(pk=int(order))
        except Exception as e:
            return Response("No order found with such id", 400)
        try:
            customer_obj = Customer.objects.get(pk=int(customer))
        except Exception:
            return Response("No customer found with that id", 400)
        
        order_obj.customer = customer_obj
        order_obj.save()

        return Response("Customer has been updated successfully", 200)

from order.utils import send_bar_order_notification_socket, send_order_notification_socket
from datetime import datetime, timedelta
class CompleteOrderDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        completed_orderdetail = data['completed_orderdetail']
        # Get the current time and format it as a string (HH:MM:SS)
        completed_time_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        completed_by = data['completed_by']
        # device = data['device']

        for comporderdetail in completed_orderdetail:
            try:
                orderdetail = tblOrderTracker.objects.get(pk= int(comporderdetail))

                print(f'orderdetail {orderdetail}')
            except Exception as e:
                return Response(f"Order detail could not be found of the is {comporderdetail}", 400)
            
            if orderdetail.state == 'Normal':
                ordertime_str = orderdetail.ordertime
                avg_preptime_str = orderdetail.average_prep_time
                # from datetime import datetime
                if ordertime_str:
                    # Parse ordertime and completed_time
                    order_datetime = datetime.strptime(ordertime_str, "%Y-%m-%d %I:%M:%S %p")
                    # average_preptime = datetime.strptime(avg_preptime_str, "%Y-%m-%d %I:%M %p")
                    completed_time = datetime.strptime(completed_time_str, "%Y-%m-%d %I:%M:%S %p")

                    # Calculate the total time difference
                    total_time_delta = completed_time - order_datetime

                    # prep_time_delta = average_preptime - total_time_delta

                    # Convert the difference to total seconds and format it as HH:MM:SS
                    total_seconds = int(total_time_delta.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    total_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

                    orderdetail.total_time = total_time_str

                    # Calculate average preparation time
                    if avg_preptime_str:
                        average_prep_time = datetime.strptime(avg_preptime_str, "%H:%M:%S")
                        avg_prep_timedelta = timedelta(hours=average_prep_time.hour, minutes=average_prep_time.minute, seconds=average_prep_time.second)

                        # Calculate the prep time difference
                        prep_time_difference =  avg_prep_timedelta - total_time_delta 

                        # Check if the difference is negative
                        if prep_time_difference < timedelta(0):
                            prep_time_diff_seconds = int(abs(prep_time_difference.total_seconds()))  # Take the absolute value for display
                            prep_time_str = f"−{str(timedelta(seconds=prep_time_diff_seconds))}"  # Add negative sign
                        else:
                            prep_time_diff_seconds = int(prep_time_difference.total_seconds())
                            prep_time_str = str(timedelta(seconds=prep_time_diff_seconds))

                        orderdetail.prep_time_difference = prep_time_str
                orderdetail.is_completed = True
                orderdetail.done = True
                orderdetail.employee = completed_by
                print(f"completed_by {completed_by}")
                orderdetail.completed_from = "OrderTracker"
                orderdetail.completed_time = completed_time_str
                orderdetail.save()
            else:
                    completed_time = datetime.strptime(completed_time_str, "%Y-%m-%d %I:%M:%S %p")
                    orderdetail.completed_time = completed_time_str
                    orderdetail.done = True
                    orderdetail.completed_from = "OrderTracker"
                    orderdetail.save()



        # order = orderdetail.order
        # if order.tblordertracker_set.filter(~Q(kotID=None)).exists():
        #     if not order.tblordertracker_set.filter(~Q(botID=None)).exists():
        #         send_order_notification_socket(orderdetail.order.branch.branch_code)
        # if order.tblordertracker_set.filter(~Q(botID=None)).exists():

        #     if not order.tblordertracker_set.filter(~Q(kotID=None) ).exists():
        #         send_bar_order_notification_socket(orderdetail.order.branch.branch_code)
        # if order.tblordertracker_set.filter(~Q(botID=None)).exists():

        #     if  order.tblordertracker_set.filter(~Q(kotID=None) ).exists():

        #         send_order_notification_socket(orderdetail.order.branch.branch_code)
        #         send_bar_order_notification_socket(orderdetail.order.branch.branch_code)

        if orderdetail.kotID:
                send_order_notification_socket(orderdetail.order.branch.branch_code)
        if orderdetail.botID:
                send_bar_order_notification_socket(orderdetail.order.branch.branch_code)

        # send_order_notification_socket(orderdetail.order.branch.branch_code)
        # send_bar_order_notification_socket(orderdetail.order.branch.branch_code)
        return Response({"detail" : "Orders has been completed successfully"}, 200)
    


class SeenAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        seen_orderdetails = data['seen_orderdetail']
        # Get the current time and format it as a string (HH:MM:SS)
        # device = data['device']

        for seenorderdetail in seen_orderdetails:
            try:
                orderdetail = tblOrderTracker.objects.get(pk= int(seenorderdetail))
            except Exception as e:
                return Response(f"Order detail could not be found of the is {seenorderdetail}", 400)
    
            orderdetail.seen = True
            orderdetail.save()

        if orderdetail.kotID:
            send_order_notification_socket(orderdetail.order.branch.branch_code)
        if orderdetail.botID:
            send_bar_order_notification_socket(orderdetail.order.branch.branch_code)
        return Response({"detail" : "Orders has been seen successfully"}, 200)
    

from organization.firebase_cron import send_delivery_notification
class TestFutureOrder(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        send_delivery_notification()
        return Response("Future Order sent", 200)