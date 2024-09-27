from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.order import OrderDetailsSerializer,OrderSerializer
from api.serializers.futureorder import FutureOrderDetailsSerializer #This is different orderserializer for futureorder
from bill.models import Order, OrderDetails, FutureOrder, FutureOrderDetails
from django.db import transaction
from organization.models import Terminal, Branch
from product.models import Product
from rest_framework.permissions import AllowAny
from decimal import Decimal


class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            order_details_data = request.data.get('order_details', [])

            for order_detail_data in order_details_data:
                order_detail_data['order'] = order.id
            order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
            if order_details_serializer.is_valid():
                order_details_serializer.save()

                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                order.delete()
                return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    # def patch(self, request, format=None):
    #     order_details_data = request.data
    #     # if not order_id:
    #     #     return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    #     for order_detail_data in order_details_data:
    #         order_id = order_detail_data.get('order')
    #         if not order_id:
    #             return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     order_details_serializer = OrderDetailsSerializer(data=request.data, many=True)
        
    #     if order_details_serializer.is_valid():
    #         with transaction.atomic():
    #             # Delete existing OrderDetails associated with the specified Order ID
    #             for order_detail_data in order_details_data:
    #                 OrderDetails.objects.filter(order=order_detail_data['order']).delete()

    #             # Save new OrderDetails
    #             order_details_serializer.save()
        
    #         future_order = FutureOrder.objects.filter(order=order_detail_data['order']).first()
    #         print(f"future_order {future_order}")
    #         if future_order:
    #             for order_detail_data in order_details_data:
    #                 FutureOrderDetails.objects.filter(order=future_order).delete()
    #                 future_data = request.data
    #                 future_data['order'] = future_order.id
    #             print(f"This is the future data {future_data}")
    #             future_order_details_serializer = FutureOrderDetailsSerializer(data=future_data, many=True)
    #             if future_order_details_serializer.is_valid():
    #                 future_order_details_serializer.save()
    #             else:
    #                 print("The data was not valid")

    #         return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
    #     else:
    #         return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        order_details_data = request.data
        # if not order_id:
        #     return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        for order_detail_data in order_details_data:
            order_id = order_detail_data.get('order')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order_details_serializer = OrderDetailsSerializer(data=request.data, many=True)
        
        if order_details_serializer.is_valid():
            with transaction.atomic():
                # Delete existing OrderDetails associated with the specified Order ID
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

            return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
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


    