from user.models import UserBranchLogin
from organization.models import Branch
from bill.models import FutureOrder
from .firebase import send_notification
from django.utils import timezone
import pytz
from django.db.models import Q
import json
    

def send_delivery_notification():
    # orders = FutureOrder.objects.filter(is_saved=True, is_completed=False, status=True, is_deleted =False, delivery_time__isnull=False)
    ny_timezone = pytz.timezone('Asia/Kathmandu')

    current_datetime_ny = timezone.now().astimezone(ny_timezone)
    formatted_datetime = current_datetime_ny.strftime("%Y-%m-%d %I:%M %p")
    print(f"This is the current datetime {formatted_datetime}")
    
    token = 'cDqGfGJ3TN6yxwMLFJrA8N:APA91bGIQCEhbwrfwVLIPV3qh4Gn9BXqY6BfVZGR6i9npL8JmaFi-9ii13L2t3KMCWSElgg0Nh43pJ96f34SfC2pCHfBT2xi9jopX8bd_XhPHfCFJEzi0EvNoeIBuSNRESJLNxV_3h7y'

    
    send_notification(token, "Delivery needs to be done", "You have a new order",{"holder":"order"})

    # if orders:
    #     for order in orders:
    #         if formatted_datetime == order.delivery_time:
    #             branch = order.branch
    #             if branch is not None:
    #             # branch=Branch.objects.first()
    #                 active_users = UserBranchLogin.objects.filter(branch=branch)
                        
    #                 if active_users:
    #                     for user in active_users:

    #                         order_type = order.order_type
    #                         table_no = order.table_no
    #                         dateTime = order.start_datetime
    #                         employee = order.employee
    #                         noOfGuest = order.no_of_guest
    #                         kotID = int(order.orderdetails_set.first().botID) if (order.orderdetails_set.first() is not None and order.orderdetails_set.first().botID is not None)else None
    #                         botID = int(order.orderdetails_set.first().kotID) if (order.orderdetails_set.first() is not None and order.orderdetails_set.first().kotID is not None)else None
    #                         token = user.device_token

    #                         order_dict = {
    #                             "orderType": order_type,
    #                             "tableNo": table_no,
    #                             "dateTime": dateTime,
    #                             "Employee": employee,
    #                             "noOfGuest": noOfGuest, 
    #                             "kotID": kotID,
    #                             "botID": botID,
    #                             "products": []


    #                         }

    #                         for order_details in order.futureorderdetails_set.all():
            
    #                             products_dict = {
    #                                 "id": order_details.id,
    #                                 "title": order_details.product.title if order_details.product else None,
    #                                 "slug": order_details.product.slug if order_details.product else None,
    #                                 "description": order_details.product.description if (order_details.product and order_details.product.description) else None,
    #                                 "unit": order_details.product.unit if (order_details.product and order_details.product.unit) else None,
    #                                 "price": order_details.product.price if (order_details.product and order_details.product.price) else None,
    #                                 "isTaxable": order_details.product.is_taxable if (order_details.product and order_details.product.is_taxable) else None,
    #                                 "discount_exempt": order_details.product.discount_exempt if (order_details.product and order_details.product.discount_exempt) else None,
    #                                 "productId": order_details.product.id if (order_details.product) else None,
    #                                 "saleId": order.sale_id,
    #                                 "product_quantity": order_details.product_quantity,
    #                                 "kotID": int(order_details.kotID) if order_details.kotID is not None else None,
    #                                 "botID": int(order_details.botID) if order_details.botID is not None else None,
    #                                 "modification": order_details.modification,
    #                                 "ordertime": order_details.ordertime,
    #                                 "employee": order_details.employee,
    #                                 "order": order.id if order is not None else None,
    #                                 "product": order_details.product.id if order_details.product else None,
    #                                 "category": order_details.product.type.title if order_details.product else None,
    #                                 "group": order_details.product.group if order_details.product else None
    #                             }

    #                             order_dict["products"].append(products_dict)

    #                         final_msg = str("You have a new order.")

    #                         if token is not None or token != '':
    #                             send_notification(token, "Delivery needs to be done", final_msg, order_dict)
    #                         else:
    #                             print("The token is None")
    #                             # else:
    #                             #     print(f"No delivery_details found !!")
    #                 else:
    #                     print(f"No active users in the branch {branch}")