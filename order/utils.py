from django.db.models.signals import post_save
from user.models import UserLogin, UserBranchLogin
from django.dispatch import receiver
from order.firebase import send_notification
from menu.models import FlagMenu


# def send_delivery_notification():
#     orders = FutureOrder.objects.filter(is_saved=True, is_completed=False, status=True, is_deleted =False, converted_to_normal=False)
#     ny_timezone = pytz.timezone('Asia/Kathmandu')

#     current_datetime_ny = timezone.now().astimezone(ny_timezone)
#     formatted_datetime = current_datetime_ny.strftime("%Y-%m-%d %I:%M %p")
#     print(f"This is the current datetime {formatted_datetime}")

#     if orders:
#         for order in orders:
#             if formatted_datetime == order.delivery_time:
#                 branch = order.branch
#                 if branch is not None:
#                 # branch=Branch.objects.first()
#                     active_users = UserBranchLogin.objects.filter(branch=branch)
                        
#                     if active_users:
#                         for user in active_users:

#                             order_type = order.order_type if order.order_type else ""
#                             order_id = order.id 
#                             special_instruction = order.special_instruction if order.special_instruction else ""
#                             table_no = order.table_no if order.table_no else ""
#                             dateTime = order.start_datetime if order.start_datetime else ""
#                             employee = order.employee if order.employee else ""
#                             noOfGuest = order.no_of_guest if order.no_of_guest else ""
#                             customer = order.customer.id if order.customer else ""
#                             kotID = int(order.futureorderdetails_set.first().botID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().botID is not None)else ""
#                             botID = int(order.futureorderdetails_set.first().kotID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().kotID is not None)else ""
#                             token = user.device_token
#                             terminal = order.terminal_no if order.terminal_no else "" 

#                             order_dict = {}
                            
#                             if order_type is not None:
#                                 order_dict["orderType"] = order_type
                                
#                             if order_id is not None:
#                                 order_dict["id"] = str(order_id)
                                
#                             if special_instruction is not None:
#                                 order_dict["special_instruction"] = str(special_instruction)

#                             if table_no is not None:
#                                 order_dict["tableNo"] = str(table_no)

#                             if dateTime is not None:
#                                 order_dict["dateTime"] = dateTime

#                             if employee is not None:
#                                 order_dict["Employee"] = employee

#                             if noOfGuest is not None:
#                                 order_dict["noOfGuest"] = str(noOfGuest)

#                             if kotID is not None:
#                                 order_dict["kotID"] = str(kotID)

#                             if botID is not None:
#                                 order_dict["botID"] = str(botID)
                                
#                             if customer is not None:
#                                 order_dict["customer_id"] = str(customer)
                                
#                             if terminal is not None:
#                                 order_dict["terminal"] = str(terminal)

#                             order_dict["products"] = []
                            
#                             for order_details in order.futureorderdetails_set.all():
            
#                                 title = order_details.product.title if order_details.product else ""
#                                 modification = order_details.modification if order_details.modification else ""
#                                 product_quantity = order_details.product_quantity if order_details.product_quantity else 0
#                                 product_id = order_details.product.id if order_details.product else ""
                                
#                                 products_dict = {}
#                                 # Check if title, modification, and product_quantity are not None
#                                 if title is not None:
#                                     products_dict['title'] = title
#                                 if modification is not None: 
#                                     products_dict['modification'] = modification
#                                 if product_quantity is not None:
#                                     products_dict['qty'] = str(product_quantity)
#                                 if product_id is not None:
#                                     products_dict['product_id'] = str(product_id)
#                                     # products_dict = {
#                                     #     "title": title,
#                                     #     "product_quantity": product_quantity,
#                                     #     "modification": modification
#                                     # }
#                                 order_dict["products"].append(products_dict)
                            
#                             order_dict["products"] = json.dumps(order_dict["products"])

#                             final_msg = f"You have a new order in terminal {str(terminal)}"
#                             # final_msg = str("You have a new order")

#                             if token is not None or token != '':
#                                 print(f"before {order_dict}")
#                                 send_notification(token, "Delivery needs to be done", final_msg, order_dict)
#                                 print(f"after {order_dict}")
#                             else:
#                                 print("The token is None")
#                                 # else:
#                                 #     print(f"No delivery_details found !!")
#                     else:
#                         print(f"No active users in the branch {branch}")

def send_delivery_notification(outlet, table_no):
    print("I am inside")
    from organization.models import Branch
    table_no =table_no
    outlet=outlet
    branch=Branch.objects.filter(branch_code=outlet, status=True, is_deleted=False).first()
    # active_users = UserLogin.objects.filter(outlet=outlet)
    active_users = UserBranchLogin.objects.filter(branch=branch)
        
    if active_users:
        for user in active_users:
            token = user.device_token
            outlet = outlet if outlet else "" 

    

            final_msg = f"You have new items added to the order in table no {str(table_no)}"

            if token is not None or token != '':

                send_notification(token, "Order needs to be received", final_msg, {"item_added": "true"})

            else:
                print("The token is None")
    else:
        print(f"No active users in the outlet {outlet}")

from product.models import Product
def get_productId(itemName):
    try:
        product_id = Product.objects.get(title=itemName).id
    except Exception as e:
        print(e)
    return product_id

from organization.models import Terminal, Table
def get_terminal(branch, table):
    terminals = Terminal.objects.filter(branch=branch, is_deleted=False, status=True)

    for terminal in terminals:
        if Table.objects.filter(terminal=terminal, table_number=table).exists():
            return terminal.terminal_no
        
    # If no matching table was found, print a message and return None
    print(f"Following table number {table} is not associated with any terminal of the branch {branch}")
    return None
    
def get_terminal_obj(branch, table):
    terminals = Terminal.objects.filter(branch=branch, is_deleted=False, status=True)

    for terminal in terminals:
        if Table.objects.filter(terminal=terminal, table_number=table).exists():
            return terminal
        
    # If no matching table was found, print a message and return None
    print(f"Following table number {table} is not associated with any terminal of the branch {branch}")
    return None
        
import json
def send_order_notification(instance, state):
    print("I am inside")
    outlet=instance.outlet
    print(outlet)
    from organization.models import Branch
    branch=Branch.objects.filter(branch_code=outlet, is_deleted=False, status=True).first()
    print(branch)
    # active_users = UserLogin.objects.filter(outlet=outlet)
    active_users = UserBranchLogin.objects.filter(branch=branch)
    print(f"active users {active_users}")
    if active_users:
        for user in active_users:

#                             order_type = order.order_type if order.order_type else ""
#                             order_id = order.id 
#                             special_instruction = order.special_instruction if order.special_instruction else ""
#                             table_no = order.table_no if order.table_no else ""
#                             dateTime = order.start_datetime if order.start_datetime else ""
#                             employee = order.employee if order.employee else ""
#                             noOfGuest = order.no_of_guest if order.no_of_guest else ""
#                             customer = order.customer.id if order.customer else ""
#                             kotID = int(order.futureorderdetails_set.first().botID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().botID is not None)else ""
#                             botID = int(order.futureorderdetails_set.first().kotID) if (order.futureorderdetails_set.first() is not None and order.futureorderdetails_set.first().kotID is not None)else ""
#                             token = user.device_token
#                             terminal = order.terminal_no if order.terminal_no else "" 

            table = instance.table_no
            terminal = get_terminal(branch, table)
            order_type = instance.type if instance.type else ""
            order_id = instance.id 
            table_no = instance.table_no if instance.table_no else ""
            dateTime = instance.start_time if instance.start_time else ""
            employee = instance.employee if instance.employee else ""
            noOfGuest = instance.noofguest if instance.noofguest else ""
            token = user.device_token
            outlet = instance.outlet if instance.outlet else "" 
            serverOrderId = instance.outlet_order if instance.outlet_order else ""
            customer_id = instance.customer.id if instance.customer else ""
            customer_name = instance.customer.name if instance.customer else ""
            mobile_number = instance.customer.phone if instance.customer else ""
            address = instance.customer.address if instance.customer else ""
            # address = instance.customer.address if instance.customer else ""
            loyalty_points = instance.customer.loyalty_points if instance.customer else "" 
            email = instance.customer.email if instance.customer else "" 

            order_dict = {}
                            
            if order_type is not None:
                order_dict["orderType"] = order_type

            if terminal is not None:
                order_dict["terminal"] = str(terminal)
                                
            if order_id is not None:
                order_dict["id"] = str(order_id)

            if table_no is not None:
                order_dict["tableNo"] = str(table_no)

            if dateTime is not None:
                order_dict["dateTime"] = dateTime

            if employee is not None:
                order_dict["Employee"] = employee

            if noOfGuest is not None:
                order_dict["noOfGuest"] = str(noOfGuest)

            if state == "Pending":
                flag = is_update_pending(instance)
                if flag == True:
                    order_dict["is_update"] = "true"    
                else:
                    order_dict["is_update"] = "false"

            if state == "Accepted":
                order_dict["is_update"] = "true"

            if state == "Normal":
                order_dict["is_update"] = "false"
            flag = FlagMenu.objects.first().autoaccept_order
            if flag == True:
                order_dict["auto_accept"] = "true"
            if flag == False:
                order_dict["auto_accept"] = "false"

            if serverOrderId is not None:
                order_dict["serverOrderId"] = str(serverOrderId)

            if customer_id is not None:
                order_dict["customer_id"] = str(customer_id)
                
            if customer_name is not None:
                order_dict["customer_name"] = str(customer_name)
            if mobile_number is not None:
                order_dict["mobile_number"] = str(mobile_number)
            if loyalty_points is not None:
                order_dict["loyalty_points"] = str(loyalty_points)
            if email is not None:
                order_dict["email"] = str(email)
            if address is not None:
                order_dict["address"] = str(address)

            order_dict["products"] = []
            order_dict["is_future"] = "false"
                            
            for order_details in instance.scanpayorderdetails_set.all():
            
                itemName = order_details.itemName if order_details.itemName else ""
                quantity = order_details.quantity if order_details.quantity else ""
                total = order_details.total if order_details.total else 0
                modification = order_details.modification if order_details.modification else ""                                
                products_dict = {}
                if itemName is not None:
                    products_dict['itemName'] = itemName
                    print(itemName)
                    productId = get_productId(itemName)
                    products_dict['product_id'] = productId
                if modification is not None: 
                    products_dict['modification'] = modification
                if quantity is not None: 
                    products_dict['quantity'] = quantity
                if total is not None:
                    products_dict['total'] = str(total)
                order_dict["products"].append(products_dict)
                            
            order_dict["products"] = json.dumps(order_dict["products"])

            final_msg = f"You have a new order in table {table_no}"

            print(token)
            if token is not None or token != '':
                print(f"before {order_dict}")
                send_payload_flag = FlagMenu.objects.first().send_payload_in_notification

                if send_payload_flag == False:
                    order_dict = {}

                send_notification(token, "Order needs to be received", final_msg, order_dict)
                print(f"after {order_dict}")
            else:
                print("The token is None")
    else:
        print(f"No active users in the outlet {outlet}")
        

from .models import ScanPayOrder, ScanPayOrderDetails
def is_update_pending(order):
    # if order
    table_no= order.table_no
    outlet= order.outlet
    if ScanPayOrder.objects.filter(table_no=table_no, outlet=outlet, state='Accepted').exists():
        flag = True
    
    else:
        flag = False
    return flag
    
from .firebase import send_redeem_notification
def send_redeemed_notification(outlet, order):
    outlet=outlet
    order=order
    from organization.models import Branch
    branch= Branch.objects.filter(branch_code=outlet, is_deleted=False, status=True).first()
    # active_users = UserLogin.objects.filter(outlet=outlet)
    active_users = UserBranchLogin.objects.filter(branch=branch)
    print(f"active users {active_users}")
    if active_users:
        for user in active_users:

            # redeemproduct = instance.redeemproduct if instance.redeemproduct else ""
            # quantity = instance.quantity 
            # customer = instance.customer if instance.customer else ""
            token = user.device_token

            # order_dict = {}
                            
            # if redeemproduct is not None:
            #     order_dict["redeemproduct"] = str(redeemproduct)
                                
            # if quantity is not None:
            #     order_dict["quantity"] = str(quantity)

            # if customer is not None:
            #     order_dict["customer"] = str(customer)

            final_msg = f"Product Redeemed"

            print(token)
            if token is not None or token != '':
                # print(f"before {order_dict}")
                send_redeem_notification(token, f"New products Reedemed in table {order.table_no}", final_msg)
                # print(f"after {order_dict}")
            else:
                print("The token is None")
    else:
        print(f"No active users in the outlet {outlet}")

# from .firebase import send_redeem_notification
# def send_redeemed_notification(outlet, order):
#     outlet=outlet
#     order=order
#     from organization.models import Branch
#     branch= Branch.objects.filter(branch_code=outlet, is_deleted=False, status=True).first()
#     # active_users = UserLogin.objects.filter(outlet=outlet)
#     active_users = UserBranchLogin.objects.filter(branch=branch)
#     # print(f"active users {active_users}")
#     if active_users:
#         for user in active_users:

#             redeemproducts = order.tblredeemedproduct_set.filter(redeemproduct__is_Menuitem=True) if order else None
#             # quantity = instance.quantity 
#             # customer = instance.customer if instance.customer else ""
#             token = user.device_token

#             order_dict = {}
#             order_dict["products"] = []
#             if redeemproducts:

                            
#                 for redeemproduct in redeemproducts:
#                     # id =redeemproduct.redeemproduct.id if redeemproduct.redeemproduct.id else ""
#                     itemName = redeemproduct.redeemproduct.name if redeemproduct.redeemproduct.name else ""
#                     quantity = redeemproduct.quantity if redeemproduct.quantity else ""
#                     # total = redeemproduct.total if redeemproduct.total else 0
#                     # modification = redeemproduct.modification if redeemproduct.modification else ""                                
#                     products_dict = {}
#                     if itemName is not None:
#                         products_dict['itemName'] = itemName
#                         print(itemName)
#                         productId = get_productId(itemName)
#                         products_dict['product_id'] = productId
#                     # if modification is not None: 
#                     #     products_dict['modification'] = modification
#                     if quantity is not None: 
#                         products_dict['quantity'] = quantity
#                     # if id is not None: 
#                     #     products_dict['id'] = id
#                     # if total is not None:
#                     #     products_dict['total'] = str(total)
#                     order_dict["products"].append(products_dict)

#             final_msg = f"Product Redeemed"

#             print(token)
#             if token is not None or token != '':
#                 # print(f"before {order_dict}")
#                 send_redeem_notification(token, f"New products Reedemed in table {order.table_no}", final_msg, order_dict)
#                 print(f"after redeemed {order_dict}")
#             else:
#                 print("The token is None")
#     else:
#         print(f"No active users in the outlet {outlet}")
       
from bill.models import Order
from order.models import ScanPayOrder
from django.db.models import Q
def complete_respective_scanpayorders(order):
    order_obj = Order.objects.get(id=int(order))
    scanpayorders = ScanPayOrder.objects.filter(Q(outlet_order=order), ~Q(state='Cancelled'))
    for order in scanpayorders:
        order.state = 'Completed'
        order.save()
