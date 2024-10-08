from django.db.models.signals import post_save
from user.models import UserLogin, UserBranchLogin
from django.dispatch import receiver
from order.firebase import send_notification
from menu.models import FlagMenu

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

            token = user.device_token

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

       
from bill.models import Order
from order.models import ScanPayOrder
from django.db.models import Q
def complete_respective_scanpayorders(order):
    order_obj = Order.objects.get(id=int(order))
    scanpayorders = ScanPayOrder.objects.filter(Q(outlet_order=order), ~Q(state='Cancelled'))
    for order in scanpayorders:
        order.state = 'Completed'
        order.save()
from collections import defaultdict
import json
# from order.utils import is_update_pending
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from bill.models import OrderDetails, tblOrderTracker

    # Convert max_prep_time to "HH:MM:SS" format for the output
def seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def send_order_notification_socket(outlet):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    # kot_groups = defaultdict(lambda: {"details": [], "void_items": []}) 


    kot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None, 
            "max_prep_time": 0
        })
    from django.db.models import Q

    for order_details in tblOrderTracker.objects.filter(Q(done=False), ~Q(kotID=None), Q(product__print_display='KITCHEN'), Q(product_quantity__gt=0)).order_by('-id'):
        kot_id = order_details.kotID if order_details.kotID else "undefined"  # Default value if kotID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""
        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""              
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""  
        state = order_details.state if order_details.state else ""            
        seen = order_details.seen              
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                'kot_id': str(kot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }
        
        kot_info = kot_groups[kot_id]
        kot_info['dateTime'] = dateTime
        kot_info['seen'] = seen
        kot_info['state'] = state
        kot_info['employee'] = employee
        kot_info['order_type'] = order_type
        kot_info['noOfGuest'] = noOfGuest
        kot_info['table_no'] = str(table_no)
        kot_info['customer'] = customer
        kot_info['order_id'] = order_id

        # Update max_prep_time
        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                kot_info['max_prep_time'] = max(kot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails

        if state == "Normal":
            kot_groups[kot_id]["details"].append(item_dict)
        elif state == "Void":
            kot_groups[kot_id]["void_items"].append(item_dict)

    for kot_id, items in kot_groups.items():
            order_dict["products"].append({ 
                "kot_id": kot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])
            })
    # final_msg = f"You have a new order in table {table_no}"
    order_dict['type'] = 'orders'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='KITCHEN'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = len(order_dict['products'])

    group_name = f"kitchen_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )

def send_bar_order_notification_socket(outlet):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    bot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None,
            "max_prep_time": 0
        })
    from django.db.models import Q

    for order_details in tblOrderTracker.objects.filter(Q(done=False), ~Q(botID=None), Q(product__print_display='BAR'), Q(product_quantity__gt=0)).order_by('-id'):
        bot_id = order_details.botID if order_details.botID else "undefined"  # Default value if botID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        state = order_details.state if order_details.state else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""

        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""               
        seen = order_details.seen    
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""            
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                'bot_id': str(bot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }

        # Group details and void items
        bot_info = bot_groups[bot_id]
        bot_info['dateTime'] = dateTime
        bot_info['seen'] = seen
        bot_info['state'] = state
        bot_info['employee'] = employee
        bot_info['order_type'] = order_type
        bot_info['noOfGuest'] = noOfGuest
        bot_info['table_no'] = str(table_no)
        bot_info['customer'] = customer
        bot_info['order_id'] = order_id

        # if state == "Normal":
        #     bot_groups[bot_id]["details"].append(item_dict)
        # elif state == "Void":
        #     bot_groups[bot_id]["void_items"].append(item_dict)
        # Update max_prep_time
        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                bot_info['max_prep_time'] = max(bot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails
        if state == "Normal":
            bot_info["details"].append(item_dict)
        elif state == "Void":
            bot_info["void_items"].append(item_dict)

    for bot_id, items in bot_groups.items():
            order_dict["products"].append({
                "bot_id": bot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])

            })



    order_dict['type'] = 'orders'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='BAR'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = len(order_dict['products'])
    group_name = f"bar_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )

def give_last_kot_bot(bills, remaining_orders):
    kot = []
    bot = []
    if bills:
        for bill_with_order in bills:
            for orderdetails in bill_with_order.order.orderdetails_set.all():
                kot_id = int(orderdetails.kotID) if orderdetails.kotID else 0
                kot.append(kot_id)
                bot_id = int(orderdetails.botID) if orderdetails.botID else 0
                bot.append(bot_id)
    if remaining_orders:
        for order in remaining_orders:
            for orderdetails in order.orderdetails_set.all():
                kot_id = int(orderdetails.kotID) if orderdetails.kotID else 0
                kot.append(kot_id)
                bot_id = int(orderdetails.botID) if orderdetails.botID else 0
                bot.append(bot_id)

    # Sort the kot and bot lists in descending order
    sorted_kot = sorted(kot, reverse=True)
    sorted_bot = sorted(bot, reverse=True)

    last_kot = sorted_kot[0] if sorted_kot else 0
    last_bot = sorted_bot[0] if sorted_bot else 0

    return last_kot, last_bot


from bill.models import tblOrderTracker, Order, OrderDetails
from api.serializers.order import tblOrderTrackerSerializer
def check_and_insert_updated_item(orderdetails_data):
    for order_detail_data in orderdetails_data:
        order = order_detail_data['order']

    order_obj = Order.objects.get(pk=int(order))
    kot = []
    bot = []
    for orderdetails in order_obj.tblordertracker_set.all():
        kot_id = orderdetails.kotID if orderdetails.kotID else 0
        kot.append(kot_id)
        bot_id = orderdetails.botID if orderdetails.botID else 0
        bot.append(bot_id)
    new_orderdetailsfortracker = []
    notify_kitchen = False
    notify_bar = False
    # orderdetails_data_copy = orderdetails_data
    for order_detail_data in orderdetails_data:
        detail_kot = order_detail_data.get('kotID', None)
        detail_bot = order_detail_data.get('botID', None)
        if detail_kot:
            if order_detail_data['kotID'] not in kot:
                new_orderdetailsfortracker.append(order_detail_data)
                notify_kitchen = True  # Set flag for kitchen notification
                # send_updateorder_notification_socket_kitchen(Order.objects.get(pk=order_obj.id))

        if detail_bot:
            if order_detail_data['botID'] not in bot:
                new_orderdetailsfortracker.append(order_detail_data)
                notify_bar = True  # Set flag for bar notification
                # send_updateorder_notification_socket_bar(Order.objects.get(pk=order_obj.id))

    serializer = tblOrderTrackerSerializer(data=new_orderdetailsfortracker, many=True)

    if serializer.is_valid():
        serializer.save()

    # Send notifications if applicable
    if notify_kitchen:
        send_updateorder_notification_socket_kitchen(order_obj)
    if notify_bar:
        send_updateorder_notification_socket_bar(order_obj)


def send_createorder_notification_socket_bar(order):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    bot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None,
            "max_prep_time": 0
        })
    from django.db.models import Q
    for order_details in tblOrderTracker.objects.filter(Q(done=False), ~Q(botID=None), Q(product__print_display='BAR'), Q(product_quantity__gt=0), Q(order=order)):
        # bot_id = order_details.botID if order_details.botID else "undefined"  # Default value if botID is None
        bot_id = order_details.botID if order_details.botID else "undefined"  # Default value if botID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        state = order_details.state if order_details.state else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""

        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""               
        seen = order_details.seen    
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""            
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                # 'kot_id': str(bot_id),
                'bot_id': str(bot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }

        # Group details and void items
        bot_info = bot_groups[bot_id]
        bot_info['dateTime'] = dateTime
        bot_info['seen'] = seen
        bot_info['state'] = state
        bot_info['employee'] = employee
        bot_info['order_type'] = order_type
        bot_info['noOfGuest'] = noOfGuest
        bot_info['table_no'] = str(table_no)
        bot_info['customer'] = customer
        bot_info['order_id'] = order_id

        # if state == "Normal":
        #     bot_groups[bot_id]["details"].append(item_dict)
        # elif state == "Void":
        #     bot_groups[bot_id]["void_items"].append(item_dict)
        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                bot_info['max_prep_time'] = max(bot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails
        if state == "Normal":
            bot_info["details"].append(item_dict)
        elif state == "Void":
            bot_info["void_items"].append(item_dict)

    for bot_id, items in bot_groups.items():
            order_dict["products"].append({
                "bot_id": bot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])
            })



    order_dict['type'] = 'single'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='BAR'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = tblOrderTracker.objects.filter(
    Q(done=False), 
    ~Q(botID=None), 
    Q(product__print_display='KITCHEN'), 
    Q(product_quantity__gt=0), 
    Q(order=order)
).values('botID').distinct().count()

    outlet = order.branch.branch_code
    group_name = f"bar_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )

def send_createorder_notification_socket_kitchen(order):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    kot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None,
            "max_prep_time": 0
        })
    from django.db.models import Q
    for order_details in tblOrderTracker.objects.filter(Q(done=False), ~Q(kotID=None), Q(product__print_display='KITCHEN'), Q(product_quantity__gt=0), Q(order=order)):
        kot_id = order_details.kotID if order_details.kotID else "undefined"  # Default value if kotID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        state = order_details.state if order_details.state else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""

        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""               
        seen = order_details.seen    
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""            
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                'kot_id': str(kot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }

        # Group details and void items
        kot_info = kot_groups[kot_id]
        kot_info['dateTime'] = dateTime
        kot_info['seen'] = seen
        kot_info['state'] = state
        kot_info['employee'] = employee
        kot_info['order_type'] = order_type
        kot_info['noOfGuest'] = noOfGuest
        kot_info['table_no'] = str(table_no)
        kot_info['customer'] = customer
        kot_info['order_id'] = order_id

        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                kot_info['max_prep_time'] = max(kot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails
        # if state == "Normal":
        #     kot_groups[kot_id]["details"].append(item_dict)
        # elif state == "Void":
        #     kot_groups[kot_id]["void_items"].append(item_dict)
        if state == "Normal":
            kot_info["details"].append(item_dict)
        elif state == "Void":
            kot_info["void_items"].append(item_dict)

    for kot_id, items in kot_groups.items():
            order_dict["products"].append({
                "kot_id": kot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])
            })



    order_dict['type'] = 'single'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='KITCHEN'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = tblOrderTracker.objects.filter(
    Q(done=False), 
    ~Q(kotID=None), 
    Q(product__print_display='KITCHEN'), 
    Q(product_quantity__gt=0), 
    Q(order=order)
).values('kotID').distinct().count()

    outlet = order.branch.branch_code
    group_name = f"kitchen_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )

def send_updateorder_notification_socket_kitchen(order):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    kot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None,
            "max_prep_time": 0
        })
    
    ordertracker = order.tblordertracker_set.order_by('id').last()

    updated_kot = ""
    # for ordertracker in ordertrackers:
    updated_kot = ordertracker.kotID

    print(f'updated_kot is {updated_kot}')
    print(f'order is {order}')
    from django.db.models import Q
    for order_details in tblOrderTracker.objects.filter(Q(done=False), Q(kotID=updated_kot), Q(product__print_display='KITCHEN'), Q(product_quantity__gt=0), Q(order=order)):
        kot_id = order_details.kotID if order_details.kotID else "undefined"  # Default value if kotID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        state = order_details.state if order_details.state else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""

        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""               
        seen = order_details.seen    
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""            
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                'kot_id': str(kot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }

        # Group details and void items
        kot_info = kot_groups[kot_id]
        kot_info['dateTime'] = dateTime
        kot_info['seen'] = seen
        kot_info['state'] = state
        kot_info['employee'] = employee
        kot_info['order_type'] = order_type
        kot_info['noOfGuest'] = noOfGuest
        kot_info['table_no'] = str(table_no)
        kot_info['customer'] = customer
        kot_info['order_id'] = order_id

        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                kot_info['max_prep_time'] = max(kot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails
        # if state == "Normal":
        #     kot_groups[kot_id]["details"].append(item_dict)
        # elif state == "Void":
        #     kot_groups[kot_id]["void_items"].append(item_dict)
        if state == "Normal":
            kot_info["details"].append(item_dict)
        elif state == "Void":
            kot_info["void_items"].append(item_dict)

    for kot_id, items in kot_groups.items():
            order_dict["products"].append({
                "kot_id": kot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])
            })



    order_dict['type'] = 'single'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='KITCHEN'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = tblOrderTracker.objects.filter(
    Q(done=False), 
    ~Q(kotID=None), 
    Q(product__print_display='KITCHEN'), 
    Q(product_quantity__gt=0), 
    Q(order=order)
).values('kotID').distinct().count()

    outlet = order.branch.branch_code
    group_name = f"kitchen_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )
def send_updateorder_notification_socket_bar(order):
    channel_layer = get_channel_layer() 
    order_dict = {
        "products": [],  # Initialize as an empty list
        "counts":{}
    }

    # Group OrderDetails by kotID
    bot_groups = defaultdict(lambda: {
            "details": [],
            "void_items": [],
            "dateTime": "",
            "seen": False,
            "state": "",
            "employee": "",
            "order_type": "",
            "noOfGuest": 0,
            "table_no": "",
            "customer": "",
            "order_id": None,
            "max_prep_time": 0
        })
    
    ordertracker = order.tblordertracker_set.order_by('id').last()

    updated_bot = ""
    # for ordertracker in ordertrackers:
    updated_bot = ordertracker.botID

    print(f'updated_bot is {updated_bot}')
    print(f'order is {order}')
    from django.db.models import Q
    for order_details in tblOrderTracker.objects.filter(Q(done=False), Q(botID=updated_bot), Q(product__print_display='BAR'), Q(product_quantity__gt=0), Q(order=order)):
        bot_id = order_details.botID if order_details.botID else "undefined"  # Default value if kotID is None
        order_detailId = order_details.id 
        itemName = order_details.product.title if order_details.product else ""
        modification = order_details.modification if order_details.modification else ""
        quantity = order_details.product_quantity if order_details.product_quantity else 0
        product_id = order_details.product.id if order_details.product else ""  
        order_type = order_details.order.order_type if order_details.order.order_type else ""
        order_id = order_details.order.id 
        table_no = order_details.order.table_no if order_details.order.table_no else ""
        date_time_str = order_details.ordertime if order_details.ordertime else ""
        state = order_details.state if order_details.state else ""
        from datetime import datetime
        if date_time_str:
            # Parse the string into a datetime object
            datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
            # Convert it to the desired format
            dateTime = datetime_obj.strftime("%H:%M:%S")
        else:
            dateTime = ""

        employee = order_details.order.employee if order_details.order.employee else ""
        noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
        customer = order_details.order.customer.name if order_details.order.customer else ""               
        seen = order_details.seen    
        branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
        terminal = order_details.order.terminal_no if order_details.order else ""            
        item_dict = {
                'orderdetailId': order_detailId,
                'itemName': itemName,
                'modification': modification,
                'quantity': quantity,
                'product_id': product_id,
                'bot_id': str(bot_id),
                'order_type': str(order_type),
                'order_id': order_id,
                'table_no': str(table_no),
                'dateTime': str(dateTime),
                'employee': employee,
                'noOfGuest': noOfGuest,
                'customer': customer,
                'seen': seen,
                'branch' : branch ,             
                'terminal' :terminal,
                'state':state
            }

        # Group details and void items
        bot_info = bot_groups[bot_id]
        bot_info['dateTime'] = dateTime
        bot_info['seen'] = seen
        bot_info['state'] = state
        bot_info['employee'] = employee
        bot_info['order_type'] = order_type
        bot_info['noOfGuest'] = noOfGuest
        bot_info['table_no'] = str(table_no)
        bot_info['customer'] = customer
        bot_info['order_id'] = order_id

        if order_details.average_prep_time:
            try:
                    # Convert average_prep_time (e.g., "00:05:00") to total seconds
                h, m, s = map(int, order_details.average_prep_time.split(':'))
                total_seconds = h * 3600 + m * 60 + s
                bot_info['max_prep_time'] = max(bot_info['max_prep_time'], total_seconds)
            except ValueError:
                pass  # Handle the case where the conversion fails
        # if state == "Normal":
        #     bot_groups[bot_id]["details"].append(item_dict)
        # elif state == "Void":
        #     bot_groups[bot_id]["void_items"].append(item_dict)
        if state == "Normal":
            bot_info["details"].append(item_dict)
        elif state == "Void":
            bot_info["void_items"].append(item_dict)

    for bot_id, items in bot_groups.items():
            order_dict["products"].append({
                "bot_id": bot_id,
                "dateTime": items['dateTime'],
                "seen": items['seen'],
                "state": items['state'],
                "employee": items['employee'],
                "order_type": items['order_type'],
                "noOfGuest": items['noOfGuest'],
                "table_no": items['table_no'],
                "customer": items['customer'],
                "order_id": items['order_id'],
                "details": items["details"],
                "void_items": items["void_items"],
                "max_prep_time": seconds_to_hhmmss(items['max_prep_time'])
            })



    order_dict['type'] = 'single'

    from django.db.models import Sum, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Get today's date
    today = timezone.now().date()

    not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    
    cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0)
        ).count()
    from django.db.models import Sum
    total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(product__print_display='BAR'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

    order_dict['counts']['not_seen'] = not_seen
    order_dict['counts']['cooking'] = cooking
    order_dict['counts']['cooked'] = cooked
    order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

    order_dict['counts']['total_order_today'] = tblOrderTracker.objects.filter(
    Q(done=False), 
    ~Q(botID=None), 
    Q(product__print_display='BAR'), 
    Q(product_quantity__gt=0), 
    Q(order=order)
).values('botID').distinct().count()

    outlet = order.branch.branch_code
    group_name = f"bar_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": order_dict # The message you want to send
        }
    )

# def send_updateorder_notification_socket_bar(order):
#     channel_layer = get_channel_layer() 
#     order_dict = {
#         "products": [],  # Initialize as an empty list
#         "counts":{}
#     }

#     # Group OrderDetails by botID
#     bot_groups = defaultdict(lambda: {
#             "details": [],
#             "void_items": [],
#             "dateTime": "",
#             "seen": False,
#             "state": "",
#             "employee": "",
#             "order_type": "",
#             "noOfGuest": 0,
#             "table_no": "",
#             "customer": "",
#             "order_id": None
#         })
#     ordertrackers = order.tblordertracker_set.all()    
#     updated_bot = ""
#     for ordertracker in ordertrackers:
#         updated_bot = ordertracker.botID
#     from django.db.models import Q
#     for order_details in tblOrderTracker.objects.filter(Q(done=False), Q(botID=updated_bot), Q(product__print_display='BAR'), Q(product_quantity__gt=0), Q(order=order)):
#         bot_id = order_details.botID if order_details.botID else "undefined"  # Default value if botID is None
#         kot_id = order_details.kotID if order_details.kotID else "undefined"  # Default value if kotID is None
#         order_detailId = order_details.id 
#         itemName = order_details.product.title if order_details.product else ""
#         modification = order_details.modification if order_details.modification else ""
#         quantity = order_details.product_quantity if order_details.product_quantity else 0
#         product_id = order_details.product.id if order_details.product else ""  
#         order_type = order_details.order.order_type if order_details.order.order_type else ""
#         order_id = order_details.order.id 
#         table_no = order_details.order.table_no if order_details.order.table_no else ""
#         date_time_str = order_details.ordertime if order_details.ordertime else ""
#         state = order_details.state if order_details.state else ""
#         from datetime import datetime
#         if date_time_str:
#             # Parse the string into a datetime object
#             datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
            
#             # Convert it to the desired format
#             dateTime = datetime_obj.strftime("%H:%M:%S")
#         else:
#             dateTime = ""

#         employee = order_details.order.employee if order_details.order.employee else ""
#         noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
#         customer = order_details.order.customer.name if order_details.order.customer else ""               
#         seen = order_details.seen    
#         branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
#         terminal = order_details.order.terminal_no if order_details.order else ""            
#         item_dict = {
#                 'orderdetailId': order_detailId,
#                 'itemName': itemName,
#                 'modification': modification,
#                 'quantity': quantity,
#                 'product_id': product_id,
#                 'kot_id': str(kot_id),
#                 'bot_id': str(bot_id),
#                 'order_type': str(order_type),
#                 'order_id': order_id,
#                 'table_no': str(table_no),
#                 'dateTime': str(dateTime),
#                 'employee': employee,
#                 'noOfGuest': noOfGuest,
#                 'customer': customer,
#                 'seen': seen,
#                 'branch' : branch ,             
#                 'terminal' :terminal,
#                 'state':state
#             }

#         # Group details and void items
#         bot_info = bot_groups[bot_id]
#         bot_info['dateTime'] = dateTime
#         bot_info['seen'] = seen
#         bot_info['state'] = state
#         bot_info['employee'] = employee
#         bot_info['order_type'] = order_type
#         bot_info['noOfGuest'] = noOfGuest
#         bot_info['table_no'] = str(table_no)
#         bot_info['customer'] = customer
#         bot_info['order_id'] = order_id

#         # if state == "Normal":
#         #     bot_groups[bot_id]["details"].append(item_dict)
#         # elif state == "Void":
#         #     bot_groups[bot_id]["void_items"].append(item_dict)
#         if state == "Normal":
#             bot_info["details"].append(item_dict)
#         elif state == "Void":
#             bot_info["void_items"].append(item_dict)

#     for bot_id, items in bot_groups.items():
#             order_dict["products"].append({
#                 "bot_id": bot_id,
#                 "dateTime": items['dateTime'],
#                 "seen": items['seen'],
#                 "state": items['state'],
#                 "employee": items['employee'],
#                 "order_type": items['order_type'],
#                 "noOfGuest": items['noOfGuest'],
#                 "table_no": items['table_no'],
#                 "customer": items['customer'],
#                 "order_id": items['order_id'],
#                 "details": items["details"],
#                 "void_items": items["void_items"]
#             })



#     order_dict['type'] = 'single'

#     from django.db.models import Sum, Q
#     from django.db.models.functions import TruncDate
#     from django.utils import timezone

#     # Get today's date
#     today = timezone.now().date()

#     not_seen = tblOrderTracker.objects.filter(
#             Q(seen=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0)
#         ).count()
#     cooking = tblOrderTracker.objects.filter(
#             Q(seen=True),
#             Q(done=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0)
#         ).count()
    
#     cooked = tblOrderTracker.objects.filter(
#             Q(done=True),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0)
#         ).count()
#     from django.db.models import Sum
#     total_void_quantity = tblOrderTracker.objects.filter(
#             Q(state='Void'), 
#             Q(product__print_display='BAR'),
#             Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
#             ).aggregate(total_quantity=Sum('product_quantity'))    

#     order_dict['counts']['not_seen'] = not_seen
#     order_dict['counts']['cooking'] = cooking
#     order_dict['counts']['cooked'] = cooked
#     order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

#     order_dict['counts']['total_order_today'] = tblOrderTracker.objects.filter(
#     Q(done=False), 
#     ~Q(botID=None), 
#     Q(product__print_display='KITCHEN'), 
#     Q(product_quantity__gt=0), 
#     Q(order=order)
# ).values('botID').distinct().count()

#     outlet = order.branch.branch_code
#     group_name = f"bar_group_{outlet}"
#     async_to_sync(channel_layer.group_send)(
#         group_name,  # The name of the group you're sending the message to
#         {
#             "type": "chat_message",
#             "message": order_dict # The message you want to send
#         }
#     )
