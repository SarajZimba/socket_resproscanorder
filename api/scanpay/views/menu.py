# from rest_framework.views import APIView
# from rest_framework.response import Response
# from menu.models import Menu
# from api.scanpay.serializers.menu import MenuSerializerCreate, MenuSerializerList, MenuTypeSerializerList, MenuTypeSerializerListOutletWise
# from menu.models import MenuType, FlagMenu

# class MenuListViewAllOutlet(APIView):
#     def get(self, request, *args, **kwargs):

#         menus = Menu.objects.filter(status=True,is_deleted=False)
#         try:    
#             serializer = MenuSerializerList(menus, many=True)
#             data = serializer.data
#             return Response(data, 200)

#         except Exception as e:
#             print(e)
#             return Response("Something went wrong", 400)
        
# class MenuTypeWiseListView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')

#         flagmenu = FlagMenu.objects.first()
#         if flagmenu:
#             flag = flagmenu.use_same_menu_for_multiple_outlet
#             if flag == True:
#                 menutypes = MenuType.objects.filter(is_deleted=False, status=True)

#                 menutypeswithmenus = MenuTypeSerializerList(menutypes, many=True)

#                 return Response(menutypeswithmenus.data, 200)
#             else:
#                 menutypes = MenuType.objects.filter(is_deleted=False, status=True)

#                 # Create an empty list to store serialized data
#                 serialized_data = []
                
#                 for menutype in menutypes:
#                     serializer = MenuTypeSerializerListOutletWise(menutype, context={'outlet_name': outlet_name})
#                     serialized_data.append(serializer.data)

#                 return Response(serialized_data)
#         else:
#             return Response("First create a flagmenu object in the admin panel", 400)

        
# class MenuListView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')

#         flagmenu = FlagMenu.objects.first()
#         if flagmenu:
#             flag = flagmenu.use_same_menu_for_multiple_outlet
#             if flag == True:
#                 menus = Menu.objects.filter(status=True, is_deleted=False)
#                 try:    
#                     serializer = MenuSerializerList(menus, many=True)
#                     data = serializer.data
#                     return Response(data, 200)

#                 except Exception as e:
#                     print(e)
#                     return Response("Something went wrong", 400)
#             else:
#                 menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name)

#                 try:    
#                     serializer = MenuSerializerList(menus, many=True)
#                     data = serializer.data
#                     return Response(data, 200)

#                 except Exception as e:
#                     print(e)
#                     return Response("Something went wrong", 400)
#         else:
#             return Response("First create a flagmenu object in the admin panel", 400)


# class MenuTypeProducts(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')
#         menutype_id = kwargs.get('id')
#         menutype = MenuType.objects.get(pk=menutype_id)


#         flagmenu = FlagMenu.objects.first()
#         if flagmenu:
#             flag = flagmenu.use_same_menu_for_multiple_outlet
#             if flag == True:
#                 menus = Menu.objects.filter(status=True, is_deleted=False,menutype=menutype)
#                 try:    
#                     serializer = MenuSerializerList(menus, many=True)
#                     # todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
#                     data = serializer.data
#                     return Response(data, 200)

#                 except Exception as e:
#                     print(e)
#                     return Response("Something went wrong", 400)
#             else:
#                 menus = Menu.objects.filter(status=True, is_deleted=False, outlet=outlet_name, menutype=menutype)

#                 try:
#                     serializer = MenuSerializerList(menus, many=True)
#                     data = serializer.data
#                     return Response(data, 200)

#                 except Exception as e:
#                     print(e)
#                     return Response("Something went wrong", 400)
#         else:
#             return Response("First create a flagmenu object in the admin panel", 400)




# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView


# class MenuCreateAPIView(APIView):
#     # parser_classes = (MultiPartParser, FormParser)
    
#     def post(self, request, *args, **kwargs):
#         print(f"This is the {request.data}")
#         datas = request.data  # Create a mutable copy of the request data
#         outlet = kwargs.get('outlet_name')
#         try:
#             menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet)
#             for menu in menus:
#                 menu.delete_check = False
#                 menu.save()
#         except Exception as e:
#             print(e)
#         try:
#             for data in datas:
#                 # data = data.copy()
#                 type = data.get('type', None)
#                 title = data.get('itemName', None)
#                 description = data.get('description', None)
#                 price = float(data.get('price', 0.0))
#                 group = data.get('group', None)
#                 image = data.get('image', None)  # Get the image from the request data
#                 image_bytes = data.get('image_bytes', None)
#                 discount_exempt = data.get('discountExempt', False)
#                 respro_itemId = data.get('respro_itemId', None)


#                 # Prepare the data for the serializer
#                 menu_data = {
#                     'item_name': title,
#                     'description': description,
#                     'price': price,
#                     'group': group,
#                     'thumbnail': image,  # Add the image to the menu data
#                     'discount_exempt':discount_exempt,
#                     'type':type,
#                     'outlet': outlet,
#                     'image_bytes':image_bytes, 
#                     'delete_check': True,
#                     'respro_itemId': respro_itemId
#                 }
                
#                 print(f"This is the menu data {menu_data} ")

#                 if Menu.objects.filter(item_name=title, outlet=outlet).exists():
#                     menu = Menu.objects.get(item_name=title, outlet=outlet)
#                     serializer = MenuSerializerCreate(menu, data=menu_data, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                 else:
#                     serializer = MenuSerializerCreate(data=menu_data)
#                     if serializer.is_valid():
#                         menu = serializer.save()
            
#             new_menus = Menu.objects.all()
#             for new_menu in new_menus:
#                 if new_menu.delete_check == False:
#                     new_menu.delete()
#             return Response("menu Created", status=status.HTTP_201_CREATED)
#         except Exception as e:
#             print(e)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ImageByteView(APIView):
#     def get(self, request, *args, **kwargs):
#         menu_name = kwargs.get('menu_name')
#         menu = Menu.objects.filter(item_name = menu_name).first()
#         dict = {}
#         if menu:
#             dict = {
#                 'image': menu.image_bytes 
#             }
#         return Response(dict, 200)
    
# class MenuSearchAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         keyword = request.GET.get('keyword')
#         try:
#             menus = Menu.objects.filter(item_name__icontains=keyword)
#             serializer = MenuSerializerList(menus, many=True)            
#             return Response(serializer.data, 200)
#         except Exception as e:
#             print(e)
#             return Response("Some exception occured", 400)
        

# class MenuPromotionalUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet_name')
#         data = request.data
#         item_name = data['item_name']

#         try:
#             menu = Menu.objects.get(item_name=item_name, outlet=outlet)
#         except Exception as e:
#             return Response("Something went wrong", 400)

#         if menu.is_promotional == True:
#             menu.is_promotional = False
#             menu.save()

#         if menu.is_promotional == False:
#             menu.is_promotional = True
#             menu.save()

#         return Response("promotional type changed successfully", 200)
    
# class MenuTodaySpecialUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet_name')
#         data = request.data
#         item_name = data['item_name']

#         try:
#             menu = Menu.objects.get(item_name=item_name, outlet=outlet)
#         except Exception as e:
#             return Response("Something went wrong", 400)

#         if menu.is_todayspecial == True:
#             menu.is_todayspecial = False
#             menu.save()

#         if menu.is_todayspecial == False:
#             menu.is_todayspecial = True
#             menu.save()

#         return Response(" todayspecial type changed successfully", 200)

# class MenuDetailView(APIView):
#     def get(self, request, *args, **kwargs):
#         menu_id = kwargs.get('menu_id')
#         try:
#             menu = Menu.objects.get(pk=menu_id)
#         except Exception as e:
#             return Response("Could not find the menu", 400)
#         serializer = MenuSerializerList(menu)
#         return Response(serializer.data, 200)            

# from menu.models import FlagMenu

# class FlagMenuToggleAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             flag_menu = FlagMenu.objects.first()
#             flag_menu.use_same_menu_for_multiple_outlet = not flag_menu.use_same_menu_for_multiple_outlet
#             flag_menu.save()
#             return Response({'message': 'Toggle successful'}, status=status.HTTP_200_OK)
#         except FlagMenu.DoesNotExist:
#             return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
            
# from menu.models import FlagMenu

# class OrderAutoAcceptView(APIView):
#     def post(self, request, format=None):
#         try:
#             flag_menu = FlagMenu.objects.first()
#             flag_menu.autoaccept_order = not flag_menu.autoaccept_order
#             flag_menu.save()
#             return Response({'auto_accept': flag_menu.autoaccept_order}, status=status.HTTP_200_OK)
#         except FlagMenu.DoesNotExist:
#             return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
# class AcceptStatus(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             flag_menu = FlagMenu.objects.first()
#             return Response({'auto_accept': flag_menu.autoaccept_order}, status=status.HTTP_200_OK)
#         except FlagMenu.DoesNotExist:
#             return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
# from rest_framework import generics
# from menu.models import tbl_redeemproduct
# from api.scanpay.serializers.menu import TblRedeemProductSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class TblRedeemProductListView(APIView):
#     def get(self, request, format=None):
#         """
#         Retrieve all redeem products.
#         """
#         redeem_products = tbl_redeemproduct.objects.filter(state=True)
#         serializer = TblRedeemProductSerializer(redeem_products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, format=None):
#         """
#         Create a new redeem product.
#         """
#         serializer = TblRedeemProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# from api.scanpay.serializers.menu import RedeemedProductSerializer 
# from order.utils import send_redeemed_notification
# from menu.models import TblRedeemedProduct
# from user.utils import check_points_availability, get_customer_points_after_redeemed
# from user.models import Customer
# class RedeemedProductsView(APIView):
#     def post(self, request, *args, **kwargs):

#         post_data = request.data
#         try:
#             customer = Customer.objects.get(id=int(post_data[0]['customer']))
#         except Exception as e:
#             print(e)
#         outlet = post_data[0]['outlet']

#         try:
#             from order.models import Order
#             order = Order.objects.get(id=int(post_data[0]['order']))
#         except Exception as e:
#             print(e)
#         total_points_redeemed = 0
#         for item in post_data:
#             redeemed_product = tbl_redeemproduct.objects.get(pk=item['redeemproduct'])
#             points_redeemed = int(redeemed_product.points) * item['quantity']
#             total_points_redeemed += points_redeemed
#         flag = check_points_availability(customer, total_points_redeemed, order) 
        
#         if flag == True:
#             serializer = RedeemedProductSerializer(data=request.data, many=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 send_redeemed_notification(outlet, order)

#             # for same response as the todaysredeemedproduct
#                 today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
#                 today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
                
#                 todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
#                 serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

#                 total_points_redeemed = 0
#                 for obj in todays_objects:
#                     total_points_for_obj = obj.redeemproduct.points * obj.quantity
#                     total_points_redeemed += total_points_for_obj
#                 new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

#                 data = {
#                     "todays_redeemed" : serializer.data,
#                     "new_loyalty_points": new_points
#                 }

#                 return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"data": "Customer points not sufficient"}, 400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from datetime import datetime   
# from django.utils import timezone
# from api.scanpay.serializers.menu import RedeemedProductTodaySerializer
# from order.models import ScanPayOrder
# class TodayRedeemedProducts(APIView):
    
#     def get(self, request, *args, **kwargs):
#         order = kwargs.get('order')
#         order = ScanPayOrder.objects.get(pk=order)
#         customer = order.customer
#         if order.customer:
#             today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
#             today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
            
#             # Query the database
#             todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
#             serializer = RedeemedProductTodaySerializer(todays_objects, many=True)
    
#             total_points_redeemed = 0
#             for obj in todays_objects:
#                 total_points_for_obj = obj.redeemproduct.points * obj.quantity
#                 total_points_redeemed += total_points_for_obj
#             new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)
    
#             data = {
#                 "todays_redeemed" : serializer.data,
#                 "new_loyalty_points": new_points
#             }
#             return Response(data, 200)
#         else:
#             return Response("Order does not have customer associated with it", 400)

    

# class RemoveRedeemedProducts(APIView):
#     def get(self, request, *args, **kwargs):
#         redeemedproductid = kwargs.get('id')
#         redeemedproduct = TblRedeemedProduct.objects.get(pk=redeemedproductid)
#         order = redeemedproduct.order

#         customer = order.customer
#         today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
#         today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
        
#         # Query the database
#         redeemedproduct.delete()
#         todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
#         serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

#         total_points_redeemed = 0
#         for obj in todays_objects:
#             total_points_for_obj = obj.redeemproduct.points * obj.quantity
#             total_points_redeemed += total_points_for_obj
#         new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

#         data = {
#             "todays_redeemed" : serializer.data,
#             "new_loyalty_points": new_points
#         }

#         return Response(data, 200)
        
# class RemoveAllRedeemedProducts(APIView):
#     def get(self, request, *args, **kwargs):
#         order_id = kwargs.get('order')
#         order = ScanPayOrder.objects.get(pk=order_id)
#         customer = order.customer
#         redeemedproducts = TblRedeemedProduct.objects.filter(order=order).delete()


#         if order.customer:
#             today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
#             today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
            
#             # Query the database
#             todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
#             serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

#             total_points_redeemed = 0
#             for obj in todays_objects:
#                 total_points_for_obj = obj.redeemproduct.points * obj.quantity
#                 total_points_redeemed += total_points_for_obj
#             new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

#             data = {
#                 "todays_redeemed" : serializer.data,
#                 "new_loyalty_points": new_points
#             }
#             return Response(data, 200)
#         else:
#             return Response("Order does not have customer associated with it", 400)


# class GetRedeemedProductsView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet')
#         # Filter redeemed products
#         redeemed_products = TblRedeemedProduct.objects.filter(state='Pending', outlet=outlet)
        
#         # Prepare data structure
#         table_data = {}
#         for product in redeemed_products:
#             # Get table number from order
#             table_no = product.order.table_no if product.order else None
#             customer_id = product.customer.id if product.customer else None
#             order_id = product.order.id if product.order else None 

#             # Initialize the table entry if it doesn't exist
#             if table_no not in table_data:
#                 table_data[table_no] = {
#                     "table_no": table_no,
#                     "customer_id" : customer_id,
#                     "order_id": order_id,
#                     "customer": product.customer.name if product.customer else None,
#                     "email": product.customer.email if product.customer else None, 
#                     "phone": product.customer.phone if product.customer else None, 
#                     "customerpoints": product.customer.total_points if product.customer else None,
#                     "redeemedpoints": 0.0,
#                     "remainingpoints": 0.0,

#                     "redeemed_products": []
#                 }
#             total_redeempoints = 0.0
#             # Serialize the product data
#             product_data = {
#                 "id": product.id,
#                 "quantity": product.quantity,
#                 "outlet": product.outlet,
#                 "state": product.state,
#                 "redeemproduct": product.redeemproduct.name if product.redeemproduct else None,
#                 "customer": product.customer.name,
#                 "order": product.order.id if product.order else None,
#                 "points" : product.redeemproduct.points,
#                 "price": product.redeemproduct.MenuitemID.price if product.redeemproduct.is_Menuitem else None,
#                 "total": product.redeemproduct.points * product.quantity,
#                 "menuitem_flag" : product.redeemproduct.is_Menuitem
#             }
#             table_data[table_no]["redeemedpoints"] += product.redeemproduct.points * product.quantity
#             table_data[table_no]["redeemed_products"].append(product_data)
#             table_data[table_no]["remainingpoints"] = table_data[table_no]["customerpoints"] - table_data[table_no]["redeemedpoints"]
        
#         # Convert to list format
#         result = list(table_data.values())

#         return Response(result, status=200)
        
# class PayloadToggleAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             flag_menu = FlagMenu.objects.first()
#             flag_menu.send_payload_in_notification = not flag_menu.send_payload_in_notification
#             flag_menu.save()
#             return Response({'message': 'Payload Toggle successful'}, status=status.HTTP_200_OK)
#         except FlagMenu.DoesNotExist:
#             return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
   
   
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from menu.models import tbl_timedpromomenu
# from api.scanpay.serializers.menu import TimedPromoMenuSerializer

# class CreateTimedPromoMenuView(APIView):
#     def post(self, request, *args, **kwargs):

#         menutype = request.data[0]['menutype']  
#         print(f'menutype {menutype}')
#         previous_entry = tbl_timedpromomenu.objects.filter(menutype__id = menutype)
#         print(previous_entry)
#         if previous_entry:
#             previous_entry.delete()
#         serializer = TimedPromoMenuSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             # Create or update instances in bulk
#             instances = [tbl_timedpromomenu(**item) for item in serializer.validated_data]
#             tbl_timedpromomenu.objects.bulk_create(instances)
#             return Response({"status": "success"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DiscountToggleAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             flag_menu = FlagMenu.objects.first()
#             flag_menu.allow_discount = not flag_menu.allow_discount
#             flag_menu.save()
#             return Response({'message': 'Discount Toggle successful'}, status=status.HTTP_200_OK)
#         except FlagMenu.DoesNotExist:
#             return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from menu.models import Menu
from api.scanpay.serializers.menu import MenuSerializerCreate, MenuSerializerList, MenuTypeSerializerList, MenuTypeSerializerListOutletWise
from menu.models import MenuType, FlagMenu
from rest_framework.permissions import AllowAny
# class MenuTypeWiseListView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')

#         menutypes = MenuType.objects.filter(is_deleted=False, status=True)

#         menutypeswithmenus = MenuTypeSerializerList(menutypes, many=True)

#         return Response(menutypeswithmenus.data, 200)

        
# class MenuListView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')

#         menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name)
#         try:    
#             serializer = MenuSerializerList(menus, many=True)
#             data = serializer.data
#             return Response(data, 200)

#         except Exception as e:
#             print(e)
#             return Response("Something went wrong", 400)

class MenuListViewAllOutlet(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):

        menus = Menu.objects.filter(status=True,is_deleted=False)
        try:    
            serializer = MenuSerializerList(menus, many=True)
            data = serializer.data
            return Response(data, 200)

        except Exception as e:
            print(e)
            return Response("Something went wrong", 400)
        
class MenuTypeWiseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        flagmenu = FlagMenu.objects.first()
        if flagmenu:
            flag = flagmenu.use_same_menu_for_multiple_outlet
            if flag == True:
                menutypes = MenuType.objects.filter(is_deleted=False, status=True)

                menutypeswithmenus = MenuTypeSerializerList(menutypes, many=True)

                return Response(menutypeswithmenus.data, 200)
            else:
                menutypes = MenuType.objects.filter(is_deleted=False, status=True)

                # Create an empty list to store serialized data
                serialized_data = []
                
                for menutype in menutypes:
                    serializer = MenuTypeSerializerListOutletWise(menutype, context={'outlet_name': outlet_name})
                    serialized_data.append(serializer.data)

                return Response(serialized_data)
        else:
            return Response("First create a flagmenu object in the admin panel", 400)

        
class MenuListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        flagmenu = FlagMenu.objects.first()
        if flagmenu:
            flag = flagmenu.use_same_menu_for_multiple_outlet
            if flag == True:
                menus = Menu.objects.filter(status=True, is_deleted=False)
                try:    
                    serializer = MenuSerializerList(menus, many=True)
                    # todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
                    data = serializer.data
                    return Response(data, 200)

                except Exception as e:
                    print(e)
                    return Response("Something went wrong", 400)
            else:
                menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name)

                try:    
                    serializer = MenuSerializerList(menus, many=True)
                    # todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
                    data = serializer.data
                    return Response(data, 200)

                except Exception as e:
                    print(e)
                    return Response("Something went wrong", 400)
        else:
            return Response("First create a flagmenu object in the admin panel", 400)

# class MenuTypeProducts(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet_name = kwargs.get('outlet_name')
#         menutype_id = kwargs.get('id')
#         menutype = MenuType.objects.get(pk=menutype_id)
#         menus = Menu.objects.filter(status=True, is_deleted=False, outlet=outlet_name, menutype=menutype)

#         try:
#             serializer = MenuSerializerList(menus, many=True)
#             data = serializer.data
#             return Response(data, 200)

#         except Exception as e:
#             print(e)
#             return Response("Something went wrong", 400)

class MenuTypeProducts(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')
        menutype_id = kwargs.get('id')
        menutype = MenuType.objects.get(pk=menutype_id)


        flagmenu = FlagMenu.objects.first()
        if flagmenu:
            flag = flagmenu.use_same_menu_for_multiple_outlet
            if flag == True:
                menus = Menu.objects.filter(status=True, is_deleted=False,menutype=menutype)
                try:    
                    serializer = MenuSerializerList(menus, many=True)
                    # todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
                    data = serializer.data
                    return Response(data, 200)

                except Exception as e:
                    print(e)
                    return Response("Something went wrong", 400)
            else:
                menus = Menu.objects.filter(status=True, is_deleted=False, outlet=outlet_name, menutype=menutype)

                try:
                    serializer = MenuSerializerList(menus, many=True)
                    data = serializer.data
                    return Response(data, 200)

                except Exception as e:
                    print(e)
                    return Response("Something went wrong", 400)
        else:
            return Response("First create a flagmenu object in the admin panel", 400)




from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# class MenuCreateAPIView(APIView):
#     # parser_classes = (MultiPartParser, FormParser)
    
#     def post(self, request, *args, **kwargs):
#         print(f"This is the {request.data}")
#         datas = request.data  # Create a mutable copy of the request data
#         outlet = kwargs.get('outlet_name')
#         # try:
#         #     menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet)
#         #     menus.delete()
#         # except Exception as e:
#         #     print(e)
#         try:
#             for data in datas:
#                 # data = data.copy()
#                 type = data.get('type', None)
#                 title = data.get('itemName', None)
#                 description = data.get('description', None)
#                 price = float(data.get('price', 0.0))
#                 group = data.get('group', None)
#                 image = data.get('image', None)  # Get the image from the request data
#                 image_bytes = data.get('image_bytes', None)
#                 discount_exempt = data.get('discountExempt', False)


#                 # Prepare the data for the serializer
#                 menu_data = {
#                     'item_name': title,
#                     'description': description,
#                     'price': price,
#                     'group': group,
#                     'thumbnail': image,  # Add the image to the menu data
#                     'discount_exempt':discount_exempt,
#                     'type':type,
#                     'outlet': outlet,
#                     'image_bytes':image_bytes
#                 }
                
#                 print(f"This is the menu data {menu_data} ")

#                 if Menu.objects.filter(item_name=title, outlet=outlet).exists():
#                     menu = Menu.objects.get(item_name=title, outlet=outlet)
#                     serializer = MenuSerializerCreate(menu, data=menu_data, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                 else:
#                     serializer = MenuSerializerCreate(data=menu_data)
#                     if serializer.is_valid():
#                         menu = serializer.save()
#             return Response("menu Created", status=status.HTTP_201_CREATED)
#         except Exception as e:
#             print(e)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class MenuCreateAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print(f"This is the {request.data}")
        datas = request.data  # Create a mutable copy of the request data
        outlet = kwargs.get('outlet_name')
        try:
            menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet)
            for menu in menus:
                menu.delete_check = False
                menu.save()
        except Exception as e:
            print(e)
        try:
            for data in datas:
                # data = data.copy()
                type = data.get('type', None)
                title = data.get('itemName', None)
                description = data.get('description', None)
                price = float(data.get('price', 0.0))
                group = data.get('group', None)
                image = data.get('image', None)  # Get the image from the request data
                image_bytes = data.get('image_bytes', None)
                discount_exempt = data.get('discountExempt', False)
                respro_itemId = data.get('respro_itemId', None)


                # Prepare the data for the serializer
                menu_data = {
                    'item_name': title,
                    'description': description,
                    'price': price,
                    'group': group,
                    'thumbnail': image,  # Add the image to the menu data
                    'discount_exempt':discount_exempt,
                    'type':type,
                    'outlet': outlet,
                    'image_bytes':image_bytes, 
                    'delete_check': True,
                    'respro_itemId': respro_itemId
                }
                
                print(f"This is the menu data {menu_data} ")

                if Menu.objects.filter(item_name=title, outlet=outlet).exists():
                    menu = Menu.objects.get(item_name=title, outlet=outlet)
                    serializer = MenuSerializerCreate(menu, data=menu_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                else:
                    serializer = MenuSerializerCreate(data=menu_data)
                    if serializer.is_valid():
                        menu = serializer.save()
            
            new_menus = Menu.objects.all()
            for new_menu in new_menus:
                if new_menu.delete_check == False:
                    new_menu.delete()
            return Response("menu Created", status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ImageByteView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        menu_name = kwargs.get('menu_name')
        menu = Menu.objects.filter(item_name = menu_name).first()
        dict = {}
        if menu:
            dict = {
                'image': menu.image_bytes 
            }
        return Response(dict, 200)
    
class MenuSearchAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        try:
            menus = Menu.objects.filter(item_name__icontains=keyword)
            serializer = MenuSerializerList(menus, many=True)            
            return Response(serializer.data, 200)
        except Exception as e:
            print(e)
            return Response("Some exception occured", 400)
        

class MenuPromotionalUpdateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet_name')
        data = request.data
        item_name = data['item_name']

        try:
            menu = Menu.objects.get(item_name=item_name, outlet=outlet)
        except Exception as e:
            return Response("Something went wrong", 400)

        if menu.is_promotional == True:
            menu.is_promotional = False
            menu.save()

        if menu.is_promotional == False:
            menu.is_promotional = True
            menu.save()

        return Response("promotional type changed successfully", 200)
    
class MenuTodaySpecialUpdateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet_name')
        data = request.data
        item_name = data['item_name']

        try:
            menu = Menu.objects.get(item_name=item_name, outlet=outlet)
        except Exception as e:
            return Response("Something went wrong", 400)

        if menu.is_todayspecial == True:
            menu.is_todayspecial = False
            menu.save()

        if menu.is_todayspecial == False:
            menu.is_todayspecial = True
            menu.save()

        return Response(" todayspecial type changed successfully", 200)

class MenuDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get('menu_id')
        try:
            menu = Menu.objects.get(pk=menu_id)
        except Exception as e:
            return Response("Could not find the menu", 400)
        serializer = MenuSerializerList(menu)
        return Response(serializer.data, 200)            

from menu.models import FlagMenu

class FlagMenuToggleAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            flag_menu = FlagMenu.objects.first()
            flag_menu.use_same_menu_for_multiple_outlet = not flag_menu.use_same_menu_for_multiple_outlet
            flag_menu.save()
            return Response({'message': 'Toggle successful'}, status=status.HTTP_200_OK)
        except FlagMenu.DoesNotExist:
            return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
            
from menu.models import FlagMenu

class OrderAutoAcceptView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            flag_menu = FlagMenu.objects.first()
            flag_menu.autoaccept_order = not flag_menu.autoaccept_order
            flag_menu.save()
            return Response({'auto_accept': flag_menu.autoaccept_order}, status=status.HTTP_200_OK)
        except FlagMenu.DoesNotExist:
            return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
class AcceptStatus(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            flag_menu = FlagMenu.objects.first()
            return Response({'auto_accept': flag_menu.autoaccept_order}, status=status.HTTP_200_OK)
        except FlagMenu.DoesNotExist:
            return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
            
from rest_framework import generics
from menu.models import tbl_redeemproduct
from api.scanpay.serializers.menu import TblRedeemProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TblRedeemProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        """
        Retrieve all redeem products.
        """
        redeem_products = tbl_redeemproduct.objects.filter(state=True)
        serializer = TblRedeemProductSerializer(redeem_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new redeem product.
        """
        serializer = TblRedeemProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
from api.scanpay.serializers.menu import RedeemedProductSerializer 
from order.utils import send_redeemed_notification
from menu.models import TblRedeemedProduct
from user.utils import check_points_availability, get_customer_points_after_redeemed
from user.models import Customer
class RedeemedProductsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):

        post_data = request.data
        try:
            customer = Customer.objects.get(id=int(post_data[0]['customer']))
        except Exception as e:
            print(e)
        outlet = post_data[0]['outlet']

        try:
            from order.models import ScanPayOrder
            print("order id in redeem", int(post_data[0]['order']))
            order = ScanPayOrder.objects.get(id=int(post_data[0]['order']))
        except Exception as e:
            print(e)
        total_points_redeemed = 0
        for item in post_data:
            redeemed_product = tbl_redeemproduct.objects.get(pk=item['redeemproduct'])
            points_redeemed = int(redeemed_product.points) * item['quantity']
            total_points_redeemed += points_redeemed
        flag = check_points_availability(customer, total_points_redeemed, order) 
        
        if flag == True:
            serializer = RedeemedProductSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                send_redeemed_notification(outlet, order)

            # for same response as the todaysredeemedproduct
                today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
                today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
                
                todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
                serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

                total_points_redeemed = 0
                for obj in todays_objects:
                    total_points_for_obj = obj.redeemproduct.points * obj.quantity
                    total_points_redeemed += total_points_for_obj
                new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

                data = {
                    "todays_redeemed" : serializer.data,
                    "new_loyalty_points": new_points
                }

                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"data": "Customer points not sufficient"}, 400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from datetime import datetime   
from django.utils import timezone
from api.scanpay.serializers.menu import RedeemedProductTodaySerializer
from order.models import ScanPayOrder
class TodayRedeemedProducts(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        order = kwargs.get('order')
        order = ScanPayOrder.objects.get(pk=order)
        customer = order.customer
        if order.customer:
            today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
            today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
            
            # Query the database
            todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
            serializer = RedeemedProductTodaySerializer(todays_objects, many=True)
    
            total_points_redeemed = 0
            for obj in todays_objects:
                total_points_for_obj = obj.redeemproduct.points * obj.quantity
                total_points_redeemed += total_points_for_obj
            new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)
    
            data = {
                "todays_redeemed" : serializer.data,
                "new_loyalty_points": new_points
            }
            return Response(data, 200)
        else:
            return Response("Order does not have customer associated with it", 400)

    

class RemoveRedeemedProducts(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        redeemedproductid = kwargs.get('id')
        redeemedproduct = TblRedeemedProduct.objects.get(pk=redeemedproductid)
        order = redeemedproduct.order

        customer = order.customer
        today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
        today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
        
        # Query the database
        redeemedproduct.delete()
        todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
        serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

        total_points_redeemed = 0
        for obj in todays_objects:
            total_points_for_obj = obj.redeemproduct.points * obj.quantity
            total_points_redeemed += total_points_for_obj
        new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

        data = {
            "todays_redeemed" : serializer.data,
            "new_loyalty_points": new_points
        }

        return Response(data, 200)
        
class RemoveAllRedeemedProducts(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order')
        order = ScanPayOrder.objects.get(pk=order_id)
        customer = order.customer
        redeemedproducts = TblRedeemedProduct.objects.filter(order=order).delete()


        if order.customer:
            today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
            today_end = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
            
            # Query the database
            todays_objects = TblRedeemedProduct.objects.filter(created_at__range=(today_start, today_end), order=order)
            serializer = RedeemedProductTodaySerializer(todays_objects, many=True)

            total_points_redeemed = 0
            for obj in todays_objects:
                total_points_for_obj = obj.redeemproduct.points * obj.quantity
                total_points_redeemed += total_points_for_obj
            new_points = get_customer_points_after_redeemed(customer, total_points_redeemed)

            data = {
                "todays_redeemed" : serializer.data,
                "new_loyalty_points": new_points
            }
            return Response(data, 200)
        else:
            return Response("Order does not have customer associated with it", 400)
            
# class GetRedeemedProductsView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet')
#         # Filter redeemed products
#         redeemed_products = TblRedeemedProduct.objects.filter(state='Pending', outlet=outlet)
        
#         # Prepare data structure
#         table_data = {}
#         for product in redeemed_products:
#             # Get table number from order
#             table_no = product.order.table_no if product.order else None
#             customer_id = product.customer.id if product.customer else None
            
#             # Initialize the table entry if it doesn't exist
#             if table_no not in table_data:
#                 table_data[table_no] = {
#                     "table_no": table_no,
#                     "customer": product.customer.name,
#                     "redeemed_products": []
#                 }
            
#             # Serialize the product data
#             product_data = {
#                 "id": product.id,
#                 "quantity": product.quantity,
#                 "outlet": product.outlet,
#                 "state": product.state,
#                 "redeemproduct": product.redeemproduct.name if product.redeemproduct else None,
#                 "customer": product.customer.name,
#                 "order": product.order.id if product.order else None,
#                 "points" : product.redeemproduct.points,
#                 "total": product.redeemproduct.points * product.quantity
#             }
#             table_data[table_no]["redeemed_products"].append(product_data)
        
#         # Convert to list format
#         result = list(table_data.values())

#         return Response(result, status=200)
from order.utils import get_terminal
from organization.models import Branch
from decimal import Decimal
class GetRedeemedProductsView(APIView):
    # permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet')
        branch = Branch.objects.filter(branch_code=outlet,status=True, is_deleted=False).first()
        # Filter redeemed products
        redeemed_products = TblRedeemedProduct.objects.filter(state='Pending', outlet=outlet)
        
        # Prepare data structure
        table_data = {}
        for product in redeemed_products:
            # Get table number from order
            table_no = product.order.table_no if product.order else None
            customer_id = product.customer.id if product.customer else None
            order_id = product.order.id if product.order else None 
            noofguest = product.order.noofguest if product.order else None 
            terminal = get_terminal(branch, table_no)

            # Initialize the table entry if it doesn't exist
            if table_no not in table_data:
                table_data[table_no] = {
                    "serverOrderId": product.order.outlet_order,
                    "table_no": table_no,
                    "terminal":terminal,
                    "noofguest":noofguest,
                    "customer_id" : customer_id,
                    "order_id": order_id,
                    "customer": product.customer.name if product.customer else None,
                    "email": product.customer.email if product.customer else None, 
                    "phone": product.customer.phone if product.customer else None, 
                    "customerpoints": product.customer.loyalty_points if product.customer else None,
                    "redeemedpoints": 0.0,
                    "remainingpoints": 0.0,

                    "redeemed_products": []
                }
            total_redeempoints = 0.0
            # Serialize the product data
            product_data = {
                "respro_product": product.redeemproduct.MenuitemID.resproproduct.id if product.redeemproduct.MenuitemID else None,
                "id": product.id,
                "quantity": product.quantity,
                "outlet": product.outlet,
                "state": product.state,
                "redeemproduct": product.redeemproduct.name if product.redeemproduct else None,
                "customer": product.customer.name,
                "order": product.order.id if product.order else None,
                "points" : product.redeemproduct.points,
                "price": product.redeemproduct.MenuitemID.price if product.redeemproduct.is_Menuitem else None,
                "total": product.redeemproduct.points * product.quantity,
                "menuitem_flag" : product.redeemproduct.is_Menuitem
            }
            table_data[table_no]["redeemedpoints"] += product.redeemproduct.points * product.quantity
            table_data[table_no]["redeemed_products"].append(product_data)
            table_data[table_no]["remainingpoints"] = table_data[table_no]["customerpoints"] - Decimal(table_data[table_no]["redeemedpoints"])
        
        # Convert to list format
        result = list(table_data.values())

        return Response(result, status=200)
        
class PayloadToggleAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            flag_menu = FlagMenu.objects.first()
            flag_menu.send_payload_in_notification = not flag_menu.send_payload_in_notification
            flag_menu.save()
            return Response({'message': 'Payload Toggle successful'}, status=status.HTTP_200_OK)
        except FlagMenu.DoesNotExist:
            return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)
   
   
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from menu.models import tbl_timedpromomenu
from api.scanpay.serializers.menu import TimedPromoMenuSerializer

class CreateTimedPromoMenuView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):

        menutype = request.data[0]['menutype']  
        print(f'menutype {menutype}')
        previous_entry = tbl_timedpromomenu.objects.filter(menutype__id = menutype)
        print(previous_entry)
        if previous_entry:
            previous_entry.delete()
        serializer = TimedPromoMenuSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # Create or update instances in bulk
            instances = [tbl_timedpromomenu(**item) for item in serializer.validated_data]
            tbl_timedpromomenu.objects.bulk_create(instances)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscountToggleAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            flag_menu = FlagMenu.objects.first()
            flag_menu.allow_discount = not flag_menu.allow_discount
            flag_menu.save()
            return Response({'message': 'Discount Toggle successful'}, status=status.HTTP_200_OK)
        except FlagMenu.DoesNotExist:
            return Response({'message': 'FlagMenu not found'}, status=status.HTTP_404_NOT_FOUND)