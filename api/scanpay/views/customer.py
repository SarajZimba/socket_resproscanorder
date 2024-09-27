# from user.models import Customer, CustomerNormalLogin, CustomerGoogleLogin
# from rest_framework.views import APIView
# from api.scanpay.serializers.customer import CustomerSerializer
# from rest_framework.response import Response
# from django.db import transaction
# from django.db.models import Q
# from django.contrib.auth.hashers import check_password
# from user.utils import check_email, check_email_in_normal, check_phone
# from rest_framework.exceptions import ValidationError

# class CustomerNormalRegister(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data
#         print(data)
#         email = data.get('email')
#         username = data.get('name')
#         phone = data.get('phone')
#         dob = data.get('dob')
#         data['type'] = 'Normal'
        
#         if phone is None or phone == "":
#             return Response({"data":"Phone number is required"}, 400)
#         if not username or username == "":
#             return Response({"data":"Username is required"}, 400)
#         if not dob or dob == "":
#             return Response({"data":"Date of birth is required"}, 400)
#         check_phone_status = check_phone(phone)
#         if check_phone_status == True:
#             return Response({"data":"Phone already associated with another account"}, 400)
#         password = data.pop('password')
#         if not password or password == "":
#             return Response({"data":"Password is required"}, 400)
#         serializer = CustomerSerializer(data=data)
#         if serializer.is_valid():
#             customer = serializer.save()
#         else:
#             raise ValidationError(serializer.errors)
#         customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password, phone=phone)
#         customerNormallogin.set_password(password)
#         customerNormallogin.save()
#         return Response({"data":"Customer Registered successfully"}, 200)
    
# class CustomerGoogleRegister(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data
#         email = data.get('email')
#         username = data.get('name')
#         check_email = check_email_in_normal(email)  # check if email is already associated with another account

#         if CustomerGoogleLogin.objects.filter(email=email).exists():
#             customer_googlelogin = CustomerGoogleLogin.objects.filter(email=email).first()
#             customer = customer_googlelogin.customer
#             response_data = {'customer' : {
#                 'username': customer.name,
#                 'email': customer.email,
#                 'id': customer.id,
#                 'email': customer.email,
#                 'contact_number': customer.phone,
#                 'dob': customer.dob,
#                 'exist_already': True, 
#                 'total_points':customer.total_points,
#                 'type': 'Google'

#                 # Add any other customer details you want to include
#             }}
#             return Response(response_data, 200)
#         else:
#             if check_email == True:
#                 password = data.pop('password')
#                 customer = Customer.objects.get(email=email, type='Google')
#                 customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
#                 customerGooglelogin.set_password(password)
#                 customerGooglelogin.save()
#                 response_data = {'customer' : {
#                     'username': customer.name,
#                     'email': customer.email,
#                     'id': customer.id,
#                     'email': customer.email,
#                     'contact_number': customer.phone,
#                     'dob': customer.dob,
#                     'exist_already': True,
#                     'total_points':customer.total_points


#                     # Add any other customer details you want to include
#                 }}
#                 return Response(response_data, 200)
#             else:
#                 password = data.pop('password')
#                 data['type'] = 'Google'
#                 serializer = CustomerSerializer(data=data)
#                 if serializer.is_valid():
#                     customer = serializer.save()

#                 customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
#                 customerGooglelogin.set_password(password)
#                 customerGooglelogin.save()
#                 response_data = {'customer' : {
#                     'username': customer.name,
#                     'email': customer.email,
#                     'id': customer.id,
#                     'email': customer.email,
#                     'contact_number': customer.phone,
#                     'dob': customer.dob,
#                     'exist_already': False,
#                     'total_points':customer.total_points



#                 }}
#                 return Response(response_data, 200)
    
# class CustomerNormalLoginView(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data

#         password = data.get('password')
#         phone = data.get('phone')

#         try:
#             customer_login = CustomerNormalLogin.objects.get(Q(phone=phone))

#         except CustomerNormalLogin.DoesNotExist:
#             return Response({'detail': 'Invalid credentials'}, 401)
#         if check_password(password, customer_login.password):
#             response_data = {'customer' : {
#                 'username': customer_login.username,
#                 'email': customer_login.email,
#                 'id': customer_login.customer.id,
#                 'name': customer_login.customer.name,
#                 'email': customer_login.customer.email,
#                 'contact_number': customer_login.customer.phone,
#                 # Add any other customer details you want to include
#             }}
#             return Response(response_data, 200)
#         else:
#             return Response({'detail': 'Invalid credentials'}, 401)
        
# class CustomerGoogleLoginView(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data

#         google_id = data.get('password')
#         email = data.get('email')
#         try:
#             customer_login = CustomerGoogleLogin.objects.get(email=email)
#         except CustomerGoogleLogin.DoesNotExist:
#             return Response({'detail': 'Invalid credentials'}, 401)
#         if check_password(google_id, customer_login.google_id):
#             response_data = {'customer' : {
#                 'username': customer_login.username,
#                 'email': customer_login.email,
#                 'id': customer_login.customer.id,
#                 'name': customer_login.customer.name,
#                 'email': customer_login.customer.email,
#                 'contact_number': customer_login.customer.phone,
#                 # Add any other customer details you want to include
#             }}
#             return Response(response_data, 200)
#         else:
#             return Response({'detail': 'Invalid credentials'}, 401)



# class CustomerGuestLoginCreate(APIView):
#     def post(self, request, *args, **kwargs):
#         posted_data = request.data
#         try:
#             serializer = CustomerSerializer(data=posted_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, 200)
#         except Exception as e:
#             return Response({e}, 400)
            
# class CustomerDetailsAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         customer_id = kwargs.get('id')
#         print(customer_id)

#         try:
#             customer = Customer.objects.get(pk=customer_id)

#             serializer = CustomerSerializer(customer)

#             return Response(serializer.data, 200)
#         except Exception as e:
#             return Response("Customer of entered id could not be found", 400)
            
# class CustomerAddDetailsAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         customer_id = kwargs.get('id')
#         print(customer_id)

#         try:
#             customer = Customer.objects.get(pk=customer_id)
#             data = request.data
#             dob = data.get('dob', None)
#             phone = data.get('phone', None)
#             customer.dob = dob
#             customer.phone = phone
#             customer.save()

#             return Response("dob and phone added successfully", 200)
#         except Exception as e:
#             return Response("Customer of entered id could not be found", 400)
                   
        
# from menu.models import TblRedeemedProduct
# from django.db import transaction
# class ReduceCustomerLoyaltyPoints(APIView):
    
#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         customer_id = kwargs.get('customer')
#         customer_obj = Customer.objects.get(pk=customer_id)
#         points_to_minus = data['points']
#         order = data.get('order_id', None)
#         if customer_obj.review_points > 0:
#             if customer_obj.review_points <= points_to_minus:
#                 points_to_minus -= customer_obj.review_points
#                 customer_obj.review_points = 0
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()
#             else:
#                 customer_obj.review_points -= points_to_minus
#                 customer_obj.save()
#             tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
#             for redeemedproduct in tblredeemedproducts:
#                 redeemedproduct.state = "Accepted"
#                 redeemedproduct.save()
#             return Response("Customer points updated sucessfully", 200)
        
#         else:
#             if customer_obj.loyalty_points > 0:     
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()
#             tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
#             for redeemedproduct in tblredeemedproducts:
#                 redeemedproduct.state = "Accepted"
#                 redeemedproduct.save()

#             return Response("Customer points deducted successfully")   
            
# from api.serializers.order import CustomOrderWithOrderDetailsSerializer
# from api.scanpay.serializers.menu import MenuSerializerList
# class CustomerOrderItemHistory(APIView):

#     def get(self, request, *args, **kwargs):
#         customer_id = kwargs.get("customer_id")
#         customer = Customer.objects.get(pk=customer_id)

#         if customer:
#             from menu.models import Menu
#             from order.models import Order, OrderDetails
#             customer_orders = Order.objects.filter(customer=customer)

#             print(customer_orders)
#             distinct_item_names = OrderDetails.objects.filter(order__in=customer_orders).values_list('itemName', flat=True).distinct()

#             print(distinct_item_names)
#             menus = Menu.objects.filter(item_name__in=distinct_item_names)

#             serializer = MenuSerializerList(menus, many=True)
        
#             return Response(serializer.data, 200)
        
#         else:
#             return Response("No Customer found of that id", 400)
            
            

# from decimal import Decimal
# from api.serializers.order import CustomOrderWithOrderDetailsSerializer
# from django.db.models import Sum
# class CustomerOrderHistoryDate(APIView):

#     def get(self, request, *args, **kwargs):
#         customer_id = kwargs.get("customer_id")
#         customer = Customer.objects.get(pk=customer_id)

#         if customer:
#             from order.models import Order, OrderDetails
#             orders = Order.objects.filter(customer=customer)

#             serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)


#             # Convert serializer.data to a list and create a mapping
#             order_data = {order.id: data for order, data in zip(orders, serializer.data)}

#             # Group orders by date
#             grouped_orders = {}
#             for order in orders:
#                 order_date = order.date.strftime('%Y-%m-%d')
#                 if order_date not in grouped_orders:
#                     grouped_orders[order_date] = {
#                         "date": order_date,
#                         "orders": [],
#                         "sub_total": Decimal('0'),
#                         "vat": Decimal('0'),
#                         "grand_total": Decimal('0'),
#                         "total_quantity": 0,
#                         "total_items": 0
#                     }
#                 grouped_orders[order_date]["orders"].append(order_data[order.id])

#                 # Update totals
#                 order_details = OrderDetails.objects.filter(order=order)
#                 order_sub_total = order_details.aggregate(total=Sum('total'))['total'] or Decimal('0')
#                 order_quantity = order_details.aggregate(quantity=Sum('quantity'))['quantity'] or 0
                
#                 grouped_orders[order_date]["sub_total"] += order_sub_total
#                 grouped_vat = order_sub_total * Decimal(0.13)
#                 grouped_orders[order_date]["vat"] += grouped_vat
#                 grouped_total = order_sub_total + grouped_vat
#                 grouped_orders[order_date]["grand_total"] += grouped_total
#                 grouped_orders[order_date]["total_quantity"] += order_quantity
#                 grouped_orders[order_date]["total_items"] += order_details.count()
        

#             total_inall_order_details = OrderDetails.objects.filter(order__in=orders).aggregate(total=Sum('total'))
#             totalquantity_inall_order_details = OrderDetails.objects.filter(order__in=orders).aggregate(quantity=Sum('quantity'))
#             print(totalquantity_inall_order_details)
#             total_amount = total_inall_order_details['total'] if total_inall_order_details['total'] is not None else 0
#             total_quantity = totalquantity_inall_order_details['quantity'] if totalquantity_inall_order_details['quantity'] is not None else 0
#             total_items = OrderDetails.objects.filter(order__in=orders).count()
#             vat = total_amount * Decimal(0.13)

#             if orders:
#                 print("orders", orders)
#                 first_order = orders.first()
#                 first_order_startdate = first_order.date
#                 startdate_str = first_order_startdate.strftime('%Y-%m-%d')
#                 startdatetime_str = startdate_str + " " + first_order.start_time
#                 customer_name = first_order.customer.name if first_order.customer else ""
#             else:
#                 startdatetime_str = ""
#                 customer_name = ""

#             grand_total = total_amount + vat

#             order_dict = {

#                 # "orders" : serializer.data,
#                 "orders" : list(grouped_orders.values()),
#                 "sub_total" : round(total_amount, 2),
#                 "vat" : round(vat, 2),
#                 "grand_total": round(grand_total, 2),
#                 "total_quantity": total_quantity,
#                 "total_items": total_items,
#                 "start_datetime": startdatetime_str,
#                 "customer_name" : customer_name


#             }
        
#             return Response(order_dict, 200)
        
#         else:
#             return Response("No Customer found of that id", 400)

from user.models import Customer, CustomerNormalLogin, CustomerGoogleLogin
from rest_framework.views import APIView
from api.scanpay.serializers.customer import CustomerSerializer
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from user.utils import check_email, check_email_in_normal, check_phone
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

class CustomerNormalRegister(APIView):
    
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        print(data)
        email = data.get('email')
        username = data.get('name')
        phone = data.get('phone')
        dob = data.get('dob')
        data['type'] = 'Normal'
        
        if phone is None or phone == "":
            return Response({"data":"Phone number is required"}, 400)
        if not username or username == "":
            return Response({"data":"Username is required"}, 400)
        if not dob or dob == "":
            return Response({"data":"Date of birth is required"}, 400)
        check_phone_status = check_phone(phone)
        if check_phone_status == True:
            return Response({"data":"Phone already associated with another account"}, 400)
        # check_email = check_email(email) # check if email is already associated with another account
        # if check_email == True:
        #     return Response({"data":"Email already associated with another account"}, 400)
        password = data.pop('password')
        if not password or password == "":
            return Response({"data":"Password is required"}, 400)
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            customer = serializer.save()
        else:
            raise ValidationError(serializer.errors)
        customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password, phone=phone)
        customerNormallogin.set_password(password)
        customerNormallogin.save()
        return Response({"data":"Customer Registered successfully"}, 200)
    
class CustomerGoogleRegister(APIView):

    permission_classes = [AllowAny]    

    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data
        email = data.get('email')
        username = data.get('name')
        check_email = check_email_in_normal(email)  # check if email is already associated with another account

        if CustomerGoogleLogin.objects.filter(email=email).exists():
            customer_googlelogin = CustomerGoogleLogin.objects.filter(email=email).first()
            customer = customer_googlelogin.customer
            response_data = {'customer' : {
                'username': customer.name,
                'email': customer.email,
                'id': customer.id,
                'email': customer.email,
                'contact_number': customer.phone,
                'dob': customer.dob,
                'exist_already': True, 
                'total_points':customer.total_points,
                'type': 'Google'

                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            if check_email == True:
                password = data.pop('password')
                customer = Customer.objects.get(email=email, type='Google')
                customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
                customerGooglelogin.set_password(password)
                customerGooglelogin.save()
                response_data = {'customer' : {
                    'username': customer.name,
                    'email': customer.email,
                    'id': customer.id,
                    'email': customer.email,
                    'contact_number': customer.phone,
                    'dob': customer.dob,
                    'exist_already': True,
                    'total_points':customer.total_points


                    # Add any other customer details you want to include
                }}
                return Response(response_data, 200)
            else:
                password = data.pop('password')
                data['type'] = 'Google'
                serializer = CustomerSerializer(data=data)
                if serializer.is_valid():
                    customer = serializer.save()

                customerGooglelogin = CustomerGoogleLogin.objects.create(email=email, customer = customer, google_id=password)
                customerGooglelogin.set_password(password)
                customerGooglelogin.save()
                response_data = {'customer' : {
                    'username': customer.name,
                    'email': customer.email,
                    'id': customer.id,
                    'email': customer.email,
                    'contact_number': customer.phone,
                    'dob': customer.dob,
                    'exist_already': False,
                    'total_points':customer.total_points


                    # Add any other customer details you want to include
                }}
                return Response(response_data, 200)
    
class CustomerNormalLoginView(APIView):
    
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data

        password = data.get('password')
        phone = data.get('phone')

        try:
            # customer_login = CustomerNormalLogin.objects.get(username=username)
            customer_login = CustomerNormalLogin.objects.get(Q(phone=phone))
            # if customer_login.password is None:
            #     return Response({'is_null':True}, 404)
        except CustomerNormalLogin.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, 401)
        # customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        if check_password(password, customer_login.password):
            response_data = {'customer' : {
                'username': customer_login.username,
                'email': customer_login.email,
                'id': customer_login.customer.id,
                'name': customer_login.customer.name,
                'email': customer_login.customer.email,
                'contact_number': customer_login.customer.phone,
                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            return Response({'detail': 'Invalid credentials'}, 401)
        
class CustomerGoogleLoginView(APIView):
    
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def post(self, request,*args, **kwargs):
        data = request.data

        google_id = data.get('password')
        email = data.get('email')
        try:
            # customer_login = CustomerNormalLogin.objects.get(username=username)
            customer_login = CustomerGoogleLogin.objects.get(email=email)
        except CustomerGoogleLogin.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, 401)
        # customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
        if check_password(google_id, customer_login.google_id):
            response_data = {'customer' : {
                'username': customer_login.username,
                'email': customer_login.email,
                'id': customer_login.customer.id,
                'name': customer_login.customer.name,
                'email': customer_login.customer.email,
                'contact_number': customer_login.customer.phone,
                # Add any other customer details you want to include
            }}
            return Response(response_data, 200)
        else:
            return Response({'detail': 'Invalid credentials'}, 401)

    

    
# class CustomerGoogleRegister(APIView):
#     @transaction.atomic
#     def post(self, request,*args, **kwargs):
#         data = request.data
#         print(data)
#         password = data.pop('password')
#         serializer = CustomerSerializer(data=data)
#         if serializer.is_valid():
#             customer = serializer.save()
#         email = data.get('email')
#         username = data.get('name')
#         customerNormallogin = CustomerNormalLogin.objects.create(email=email, username=username, customer = customer, password=password)
#         customerNormallogin.set_password(password)
#         customerNormallogin.save()
#         return Response("Customer Resistered in successfully", 200)


class CustomerGuestLoginCreate(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        posted_data = request.data
        try:
            serializer = CustomerSerializer(data=posted_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
        except Exception as e:
            return Response({e}, 400)
            
class CustomerDetailsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('id')
        print(customer_id)

        try:
            customer = Customer.objects.get(pk=customer_id)

            serializer = CustomerSerializer(customer)

            return Response(serializer.data, 200)
        except Exception as e:
            return Response("Customer of entered id could not be found", 400)
            
class CustomerAddDetailsAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        customer_id = kwargs.get('id')
        print(customer_id)

        try:
            customer = Customer.objects.get(pk=customer_id)
            data = request.data
            dob = data.get('dob', None)
            phone = data.get('phone', None)
            customer.dob = dob
            customer.phone = phone
            customer.save()

            return Response("dob and phone added successfully", 200)
        except Exception as e:
            return Response("Customer of entered id could not be found", 400)
            
# # this class is used to update the dob and phone added successfully or not 

# from django.db import transaction
# class ReduceCustomerLoyaltyPoints(APIView):
    
#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         customer_id = kwargs.get('customer')
#         customer_obj = Customer.objects.get(pk=customer_id)
#         points_to_minus = data['points']
#         if customer_obj.review_points > 0:
#             if customer_obj.review_points <= points_to_minus:
#                 points_to_minus -= customer_obj.review_points
#                 customer_obj.review_points = 0
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()
#             else:
#                 customer_obj.review_points -= points_to_minus
#                 customer_obj.save()
            
#             return Response("Customer points updated sucessfully", 200)
        
#         else:
#             if customer_obj.loyalty_points > 0:     
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()

#             return Response("Customer points deducted successfully")           
        
# from menu.models import TblRedeemedProduct
# from django.db import transaction
# class ReduceCustomerLoyaltyPoints(APIView):
    
#     permission_classes = [AllowAny]
    
#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         customer_id = kwargs.get('customer')
#         customer_obj = Customer.objects.get(pk=customer_id)
#         points_to_minus = data['points']
#         order = data.get('order_id', None)
#         if customer_obj.review_points > 0:
#             if customer_obj.review_points <= points_to_minus:
#                 points_to_minus -= customer_obj.review_points
#                 customer_obj.review_points = 0
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()
#             else:
#                 customer_obj.review_points -= points_to_minus
#                 customer_obj.save()
#             tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
#             for redeemedproduct in tblredeemedproducts:
#                 redeemedproduct.state = "Accepted"
#                 redeemedproduct.save()
#             return Response("Customer points updated sucessfully", 200)
        
#         else:
#             if customer_obj.loyalty_points > 0:     
#                 if customer_obj.loyalty_points < points_to_minus:
#                     return Response("This customer does not have the points to minus", 400)
#                 customer_obj.loyalty_points -= points_to_minus
#                 customer_obj.save()
#             tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
#             for redeemedproduct in tblredeemedproducts:
#                 redeemedproduct.state = "Accepted"
#                 redeemedproduct.save()

#             return Response("Customer points deducted successfully")   
from user.utils import reduce_redeemedproducts_from_normalandscanpay

from menu.models import TblRedeemedProduct
from django.db import transaction
class ReduceCustomerLoyaltyPoints(APIView):
    
    permission_classes = [AllowAny]
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = kwargs.get('customer')
        customer_obj = Customer.objects.get(pk=customer_id)
        points_to_minus = data['points']
        order = data.get('order_id', None)
            # if customer_obj.loyalty_points < points_to_minus:

            #     customer_obj.loyalty_points -= points_to_minus
            #     customer_obj.save()
            # else:
            #     customer_obj.review_points -= points_to_minus
            #     customer_obj.save()
            # tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
            # for redeemedproduct in tblredeemedproducts:
            #     redeemedproduct.state = "Accepted"
            #     redeemedproduct.save()
            # return Response("Customer points updated sucessfully", 200)
        if customer_obj.loyalty_points > Decimal(points_to_minus):     
            customer_obj.loyalty_points -= Decimal(points_to_minus)
            customer_obj.save()
            tblredeemedproducts = TblRedeemedProduct.objects.filter(order__id = int(order))
            for redeemedproduct in tblredeemedproducts:
                redeemedproduct.state = "Accepted"
                redeemedproduct.save()
                
            reduce_redeemedproducts_from_normalandscanpay(order)

            return Response("Customer points deducted successfully") 
        
        else:
            return Response("This customer does not have the points to minus", 400)
            
from api.serializers.order import CustomOrderWithOrderDetailsSerializer
from api.scanpay.serializers.menu import MenuSerializerList
class CustomerOrderItemHistory(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        customer = Customer.objects.get(pk=customer_id)

        if customer:
            from menu.models import Menu
            from order.models import ScanPayOrder, ScanPayOrderDetails
            customer_orders = ScanPayOrder.objects.filter(customer=customer, status=True)

            print(customer_orders)
            distinct_item_names = ScanPayOrderDetails.objects.filter(order__in=customer_orders).values_list('itemName', flat=True).distinct()

            print(distinct_item_names)
            menus = Menu.objects.filter(item_name__in=distinct_item_names)

            serializer = MenuSerializerList(menus, many=True)
        
            return Response(serializer.data, 200)
        
        else:
            return Response("No Customer found of that id", 400)
            
            
# For the previously ordered items for the customer in order to reorder that product again
# So basically send the orderdetails entire objects including the id and all . 
from decimal import Decimal
from api.serializers.order import CustomOrderWithOrderDetailsSerializer
from django.db.models import Sum
class CustomerOrderHistoryDate(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        customer = Customer.objects.get(pk=customer_id)

        if customer:
            from order.models import ScanPayOrder, ScanPayOrderDetails
            orders = ScanPayOrder.objects.filter(customer=customer, status=True)

            serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)


            # Convert serializer.data to a list and create a mapping
            order_data = {order.id: data for order, data in zip(orders, serializer.data)}

            # Group orders by date
            grouped_orders = {}
            for order in orders:
                order_date = order.date.strftime('%Y-%m-%d')
                if order_date not in grouped_orders:
                    grouped_orders[order_date] = {
                        "date": order_date,
                        "orders": [],
                        "sub_total": Decimal('0'),
                        "vat": Decimal('0'),
                        "grand_total": Decimal('0'),
                        "total_quantity": 0,
                        "total_items": 0
                    }
                grouped_orders[order_date]["orders"].append(order_data[order.id])

                # Update totals
                order_details = ScanPayOrderDetails.objects.filter(order=order)
                order_sub_total = order_details.aggregate(total=Sum('total'))['total'] or Decimal('0')
                order_quantity = order_details.aggregate(quantity=Sum('quantity'))['quantity'] or 0
                
                grouped_orders[order_date]["sub_total"] += order_sub_total
                grouped_vat = order_sub_total * Decimal(0.13)
                grouped_orders[order_date]["vat"] += grouped_vat
                grouped_total = order_sub_total + grouped_vat
                grouped_orders[order_date]["grand_total"] += grouped_total
                grouped_orders[order_date]["total_quantity"] += order_quantity
                grouped_orders[order_date]["total_items"] += order_details.count()
        

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

                # "orders" : serializer.data,
                "orders" : list(grouped_orders.values()),
                "sub_total" : round(total_amount, 2),
                "vat" : round(vat, 2),
                "grand_total": round(grand_total, 2),
                "total_quantity": total_quantity,
                "total_items": total_items,
                "start_datetime": startdatetime_str,
                "customer_name" : customer_name


            }
        
            return Response(order_dict, 200)
        
        else:
            return Response("No Customer found of that id", 400)

        