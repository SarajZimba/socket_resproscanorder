from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.futureorder import OrderDetailsSerializer,OrderSerializer, FutureOrderSerializer
from bill.models import FutureOrder, FutureOrderDetails
from django.db import transaction
from organization.models import Terminal, Branch
from product.models import Product
from rest_framework.permissions import AllowAny


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
            
            
    @transaction.atomic()
    def patch(self, request, format=None):
        order_details= request.data
        order_details_data = order_details.pop('order_details', [])
        order = order_details
        outer_order_id = order.get('id', None)
        
        if outer_order_id is not None:
            try: 
                instance = FutureOrder.objects.get(pk=int(order['id']))

            except FutureOrder.DoesNotExist:
                return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)

            order_serializer = OrderSerializer(instance, data=order, partial=True)
            if order_serializer.is_valid():
                order_serializer.save()

        for order_detail_data in order_details_data:
            order_id = order_detail_data.get('order')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
        if order_details_serializer.is_valid():
            with transaction.atomic():
                # Delete existing OrderDetails associated with the specified Order ID
                for order_detail_data in order_details_data:
                    FutureOrderDetails.objects.filter(order=order_detail_data['order']).delete()

                # Save new OrderDetails
                order_details_serializer.save()

            return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, format=None):
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
                    FutureOrderDetails.objects.filter(order=order_detail_data['order']).delete()

                # Save new OrderDetails
                order_details_serializer.save()

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
            original_order = FutureOrder.objects.get(id=splitted_order_id)
            original_order_details = FutureOrderDetails.objects.filter(order=splitted_order_id)
            original_order_details.delete()

            for order_detail_data in remaining_order:
                order_detail_data.pop("order")
                product_id = order_detail_data.pop("product")
                product = Product.objects.get(pk=product_id)
                order_detail_data["product"] = product

                FutureOrderDetails.objects.create(order=original_order, **order_detail_data)



            branch_id = split_order.pop("branch")
            branch = Branch.objects.get(pk=branch_id)
            
            terminal_id = split_order.pop("terminal_no")
            terminal = Terminal.objects.get(terminal_no=terminal_id, branch=branch, is_deleted=False, status=True)

            # Create order with related objects
            split_order["terminal"] = terminal   
            split_order["branch"] = branch
            split_order["terminal_no"] = terminal_id

            order_details_data = split_order.pop("order_details", [])

            order = FutureOrder.objects.create(**split_order)

    
            for order_detail_data in order_details_data:
                order_detail_data.pop("order")
                product_id = order_detail_data.pop("product")
                product = Product.objects.get(pk=product_id)
                order_detail_data["product"] = product

                FutureOrderDetails.objects.create(order=order, **order_detail_data)

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

            order_obj = FutureOrder.objects.get(pk=int(order))
        except Exception as e:
            return Response("No order found with such id", 400)
        try:
            customer_obj = Customer.objects.get(pk=int(customer))
        except Exception:
            return Response("No customer found with that id", 400)
        
        order_obj.customer = customer_obj
        order_obj.save()

        return Response("Customer has been updated successfully", 200)
        
import jwt
from collections import defaultdict
class FutureOrderList(APIView):
    def get(self, request, *args, **kwargs):

        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")
            terminal = token_data.get("terminal")
            agent = token_data.get("name")

            # Print the branch
            print("Branch:", branch)
            print("Terminal:", terminal)
            print("Agent:", agent)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        futureorders = FutureOrder.objects.filter(is_deleted=False, status=True, branch__id=branch, terminal_no=terminal, converted_to_normal=False, is_completed=False, is_saved=True)
        
        order_type_groups = defaultdict(list)

        # Iterate over the queryset and group by order_type
        for order in futureorders:
            order_type = order.order_type
            serialized_order = FutureOrderSerializer(order).data  # Serialize each FutureOrder object
            order_type_groups[order_type].append(serialized_order)
        
        # print(f"Futureorder {futureorders}")
        # serializer = OrderSerializer(futureorders, many=True)

        return Response(order_type_groups, 200)
        # return Response(serializer.data, 200)
        
class FutureOrderDetailsList(APIView):
    def get(self, request, *args, **kwargs):
        
        futureorder_id = kwargs.get('futureorder_id')
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")
            terminal = token_data.get("terminal")
            agent = token_data.get("name")

            # Print the branch
            print("Branch:", branch)
            print("Terminal:", terminal)
            print("Agent:", agent)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        
        try:
            futureorder = FutureOrder.objects.get(id=futureorder_id)
            futureorder_details = FutureOrderDetails.objects.filter(order=futureorder, status=True)
            print(f"Futureorder {futureorder}")
            serializer = OrderDetailsSerializer(futureorder_details, many=True)
            return Response(serializer.data, status=200)
        
        except FutureOrder.DoesNotExist:
            return Response({"error": "FutureOrder does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class FutureOrderUpdateAPIView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            instance = FutureOrder.objects.get(pk=pk)
        except FutureOrder.DoesNotExist:
            return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FutureToNormalOrderUpdateAPIView(APIView):
#     def post(self, request, pk, *args, **kwargs):
#         try:
#             instance = FutureOrder.objects.get(pk=pk)
#         except FutureOrder.DoesNotExist:
#             return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         instance.converted_to_normal = True
#         instance.save()
#         return Response("Future order changed to normal", status=status.HTTP_200_OK)

# from bill.models import Bill
# class FutureToCompletedOrderUpdateAPIView(APIView):
#     def post(self, request, pk, *args, **kwargs):
#         try:
#             instance = FutureOrder.objects.get(pk=pk)
#         except FutureOrder.DoesNotExist:
#             return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)
#         data = request.data
#         invoice_number = data['invoice_number']
#         fiscal_year = data['fiscal_year']

#         bill = Bill.objects.get(fiscal_year=fiscal_year, invoice_number=invoice_number)
#         instance.bill=bill        
#         instance.is_completed = True
#         instance.is_saved=False
#         instance.save()
#         return Response("Future order completed successfully", status=status.HTTP_200_OK)

from bill.models import Order
class FutureToNormalOrderUpdateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, pk, normalorder, *args, **kwargs):
        try:
            instance = FutureOrder.objects.get(pk=pk)
        except FutureOrder.DoesNotExist:
            return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)
        try:

            order = Order.objects.get(id=normalorder)

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        instance.order = order
        instance.converted_to_normal = True
        instance.save()
        return Response("Future order changed to normal", status=status.HTTP_200_OK)

from bill.models import Bill
class FutureToCompletedOrderUpdateAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            order_instance = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            future_instance = FutureOrder.objects.get(order=order_instance)
        except FutureOrder.DoesNotExist:
            return Response({"error": "FutureOrder not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        invoice_number = data['invoice_number']
        fiscal_year = data['fiscal_year']

        bill = Bill.objects.get(fiscal_year=fiscal_year, invoice_number=invoice_number)
        future_instance.bill=bill
        future_instance.is_completed = True
        future_instance.is_saved=False
        future_instance.save()
        return Response("Future order completed successfully", status=status.HTTP_200_OK)
        
class FutureToCancelledOrderUpdateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        futureorder_id = kwargs.get('pk')
        try:
            futureorder = FutureOrder.objects.get(id=futureorder_id)
        except FutureOrder.DoesNotExist:
            return Response("No future order found having such id", 400)
        futureorder.status = False
        futureorder.is_deleted = True
        futureorder.save()
        return Response("Future order has been cancelled", 200)
        
    # class FutureOrderUpdatetoNormal(APIView):
    #     def patch(self, request, *args, **kwargs):
    #         order = data.get('order', None)
    #         data = request.data

    #         for orderdetails in data['orderdetails']:
    #             orderdetails['order'] = order