from user.models import UserBranchLogin
from organization.models import Branch
from bill.models import FutureOrder
from .firebase import send_notification
from django.utils import timezone
import pytz
from django.db.models import Q
import json
    

# def send_delivery_notification():
#     # orders = FutureOrder.objects.filter(is_saved=True, is_completed=False, status=True, is_deleted =False, delivery_time__isnull=False)
#     ny_timezone = pytz.timezone('Asia/Kathmandu')

#     current_datetime_ny = timezone.now().astimezone(ny_timezone)
#     formatted_datetime = current_datetime_ny.strftime("%Y-%m-%d %I:%M %p")
#     print(f"This is the current datetime {formatted_datetime}")
    
#     token = 'cDqGfGJ3TN6yxwMLFJrA8N:APA91bGIQCEhbwrfwVLIPV3qh4Gn9BXqY6BfVZGR6i9npL8JmaFi-9ii13L2t3KMCWSElgg0Nh43pJ96f34SfC2pCHfBT2xi9jopX8bd_XhPHfCFJEzi0EvNoeIBuSNRESJLNxV_3h7y'

    
#     send_notification(token, "Delivery needs to be done", "You have a new order", {"orderType": "Dine In"})


def send_delivery_notification():
    orders = FutureOrder.objects.filter(is_saved=True, is_completed=False, status=True, is_deleted =False, converted_to_normal=False)
    ny_timezone = pytz.timezone('Asia/Kathmandu')

    current_datetime_ny = timezone.now().astimezone(ny_timezone)
    formatted_datetime = current_datetime_ny.strftime("%Y-%m-%d %I:%M %p")
    print(f"This is the current datetime {formatted_datetime}")

    if orders:
        for order in orders:
            if formatted_datetime == order.delivery_time:
                branch = order.branch
                if branch is not None:
                # branch=Branch.objects.first()
                    active_users = UserBranchLogin.objects.filter(branch=branch)
                        
                        
                    if active_users:
                        for user in active_users:

                            order_type = order.order_type if order.order_type else ""
                            order_id = order.id 
                            special_instruction = order.special_instruction if order.special_instruction else ""
                            table_no = order.table_no if order.table_no else ""
                            dateTime = order.start_datetime if order.start_datetime else ""
                            employee = order.employee if order.employee else ""
                            noOfGuest = order.no_of_guest if order.no_of_guest else ""
                            customer = order.customer.id if order.customer else ""
                            kotID = int(order.futureorderdetails_set.first().botID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().botID is not None)else ""
                            botID = int(order.futureorderdetails_set.first().kotID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().kotID is not None)else ""
                            token = user.device_token
                            terminal = order.terminal_no if order.terminal_no else "" 

                            order_dict = {}
                            
                            if order_type is not None:
                                order_dict["orderType"] = order_type
                                
                            if order_id is not None:
                                order_dict["id"] = str(order_id)
                                
                            if special_instruction is not None:
                                order_dict["special_instruction"] = str(special_instruction)

                            if table_no is not None:
                                order_dict["tableNo"] = str(table_no)

                            if dateTime is not None:
                                order_dict["dateTime"] = dateTime

                            if employee is not None:
                                order_dict["Employee"] = employee

                            if noOfGuest is not None:
                                order_dict["noOfGuest"] = str(noOfGuest)

                            if kotID is not None:
                                order_dict["kotID"] = str(kotID)

                            if botID is not None:
                                order_dict["botID"] = str(botID)
                                
                            if customer is not None:
                                order_dict["customer_id"] = str(customer)
                                
                            if terminal is not None:
                                order_dict["terminal"] = str(terminal)

                            order_dict["is_future"] = "true"

                            order_dict["products"] = []
                            
                            for order_details in order.futureorderdetails_set.all():
            
                                title = order_details.product.title if order_details.product else ""
                                modification = order_details.modification if order_details.modification else ""
                                product_quantity = order_details.product_quantity if order_details.product_quantity else 0
                                product_id = order_details.product.id if order_details.product else ""
                                
                                products_dict = {}
                                # Check if title, modification, and product_quantity are not None
                                if title is not None:
                                    products_dict['title'] = title
                                if modification is not None: 
                                    products_dict['modification'] = modification
                                if product_quantity is not None:
                                    products_dict['qty'] = str(product_quantity)
                                if product_id is not None:
                                    products_dict['product_id'] = str(product_id)
                                    # products_dict = {
                                    #     "title": title,
                                    #     "product_quantity": product_quantity,
                                    #     "modification": modification
                                    # }
                                order_dict["products"].append(products_dict)
                            
                            order_dict["products"] = json.dumps(order_dict["products"])

                            final_msg = f"You have a new order in terminal {str(terminal)}"
                            # final_msg = str("You have a new order")

                            if token is not None or token != '':
                                print(f"before {order_dict}")
                                send_notification(token, "Delivery needs to be done", final_msg, order_dict)
                                print(f"after {order_dict}")
                            else:
                                print("The token is None")
                                # else:
                                #     print(f"No delivery_details found !!")
                    else:
                        print(f"No active users in the branch {branch}")