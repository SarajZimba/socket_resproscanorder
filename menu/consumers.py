import json
from channels.generic.websocket import AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the outlet from the query parameters
        self.outlet = self.scope['query_string'].decode('utf-8').split('=')[1]  # Assumes the format is `outlet=your_outlet`


        self.group_name = f"kitchen_group_{self.outlet}"
        await self.channel_layer.group_add(

            self.group_name,
            self.channel_name
        )
        await self.accept()


        order_data = await self.get_order_data(self.outlet)
        await self.send(text_data=json.dumps({'message': order_data}))
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == 'all_orders':
            order_data = await self.get_order_data(self.outlet)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': order_data
            }
            )   
        if message == 'orderhistory':
            order_data = await self.get_orderhistory_data(self.outlet)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': order_data
            }
            ) 
    
        # # Check if 'message' is a dictionary
        # if isinstance(text_data_json.get('message'), dict):
        #     product_id = text_data_json['message'].get('id')

    async def chat_message(self, event):
        print("I came here")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


    from channels.db import database_sync_to_async



    @database_sync_to_async
    def get_order_data(self, outlet):
        order_dict = {
            "products": [],  # Initialize as an empty list
            "counts": {}
        }

        # Group OrderDetails by botID
        from collections import defaultdict
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
            'max_prep_time': 0 # Initialize max_prep_time
        })
        from bill.models import tblOrderTracker
        from django.db.models import Q
        from datetime import datetime

        # Fetch relevant order details
        for order_details in tblOrderTracker.objects.filter(
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=self.outlet)
        ).order_by('-id'):
            kot_id = order_details.kotID if order_details.kotID else "undefined"
            order_detailId = order_details.id 
            itemName = order_details.product.title if order_details.product else ""
            modification = order_details.modification if order_details.modification else ""
            quantity = order_details.product_quantity if order_details.product_quantity else 0
            product_id = order_details.product.id if order_details.product else ""  
            order_type = order_details.order.order_type if order_details.order.order_type else ""
            order_id = order_details.order.id 
            table_no = order_details.order.table_no if order_details.order.table_no else ""
            date_time_str = order_details.ordertime if order_details.ordertime else ""
            
            # Handle dateTime formatting
            dateTime = ""
            if date_time_str:
                datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
                dateTime = datetime_obj.strftime("%H:%M:%S")

            employee = order_details.order.employee if order_details.order.employee else ""
            noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else 0
            customer = order_details.order.customer.name if order_details.order.customer else ""              
            seen = order_details.seen 
            branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
            terminal = order_details.order.terminal_no if order_details.order else ""                
            state = order_details.state if order_details.state else ""           

            # Prepare item dictionary
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
                'branch': branch,
                'terminal': terminal,
                'state': state
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
                kot_info["details"].append(item_dict)
            elif state == "Void":
                kot_info["void_items"].append(item_dict)

        # Build the final order_dict
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
                "max_prep_time": self.seconds_to_hhmmss(items['max_prep_time'])
            })

        order_dict['type'] = 'orders'
        from django.db.models import Sum, Q
        from django.utils import timezone

        # Get today's date
        today = timezone.now().date()

        not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
        cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
    
        cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
        from django.db.models import Sum
        total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(order__branch__branch_code=outlet),
            Q(product__print_display='KITCHEN'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

        order_dict['counts']['not_seen'] = not_seen
        order_dict['counts']['cooking'] = cooking
        order_dict['counts']['cooked'] = cooked
        order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

        order_dict['counts']['total_order_today'] = len(order_dict['products'])

        return order_dict
    

    # Convert max_prep_time to "HH:MM:SS" format for the output
    def seconds_to_hhmmss(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    @database_sync_to_async
    def get_orderhistory_data(self, outlet):
        # order_dict = {
        #     "products": [],  # Initialize as an empty list
        #     "counts": {}
        # }
        final_dict={
            "type": "orderhistory",
            "data":{
                "completed": [],
                "preparing": []
            }
        }
        # Group OrderDetails by kotID
        from collections import defaultdict
        from bill.models import tblOrderTracker
        from django.db.models import Q
        from datetime import datetime


        # Fetch relevant order details
        from django.db.models import Sum, F

        # Fetch relevant order details
        order_details_queryset_preparing = tblOrderTracker.objects.filter(
            Q(done=False),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).annotate(
            product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
            product_rate=F('rate'),
            product_group=F('product__group')  # Add this line to get the product group
        ).values(
            'product_title', 'product_rate', 'product_group'
        ).annotate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum(F('rate') * F('product_quantity'))
        ).order_by('-total_quantity')  # Order by total quantity if needed

        # Convert to a list of dictionaries
        result = [
            {
                'product_title': entry['product_title'],
                'product_rate': float(entry['product_rate']),
                'product_group': entry['product_group'],  # Include product group
                'total_quantity': float(entry['total_quantity']),
                'total_amount': float(entry['total_amount'])
            }
            for entry in order_details_queryset_preparing
        ]

        for item_dict in order_details_queryset_preparing:
        # Build the final order_dict
            final_dict["data"]["preparing"].append(
                {
                    'product_title': item_dict['product_title'],
                    'product_rate': float(item_dict['product_rate']),
                    'product_group': item_dict['product_group'],  # Include product group
                    'total_quantity': float(item_dict['total_quantity']),
                    'total_amount': float(item_dict['total_amount'])
                }
            )
        # Fetch relevant order details
        order_details_queryset_completed = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='KITCHEN'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).annotate(
            product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
            product_rate=F('rate'),
            product_group=F('product__group')  # Add this line to get the product group
        ).values(
            'product_title', 'product_rate', 'product_group'
        ).annotate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum(F('rate') * F('product_quantity'))
        ).order_by('-total_quantity')  # Order by total quantity if needed

        # Convert to a list of dictionaries
        result = [
            {
                'product_title': entry['product_title'],
                'product_rate': float(entry['product_rate']),
                'product_group': entry['product_group'],  # Include product group
                'total_quantity': float(entry['total_quantity']),
                'total_amount': float(entry['total_amount'])
            }
            for entry in order_details_queryset_completed
        ]

        print(f'order_details_queryset_completed  {order_details_queryset_completed}')
        for item_dict in order_details_queryset_completed:
        # Build the final order_dict
            final_dict["data"]["completed"].append(
                {
                    'product_title': item_dict['product_title'],
                    'product_rate': float(item_dict['product_rate']),
                    'product_group': item_dict['product_group'],  # Include product group
                    'total_quantity': float(item_dict['total_quantity']),
                    'total_amount': float(item_dict['total_amount'])
                }
            )

        return final_dict
    

import json
from channels.generic.websocket import AsyncWebsocketConsumer
class BarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the outlet from the query parameters
        self.outlet = self.scope['query_string'].decode('utf-8').split('=')[1]  # Assumes the format is `outlet=your_outlet`


        self.group_name = f"bar_group_{self.outlet}"
        await self.channel_layer.group_add(

            self.group_name,
            self.channel_name
        )
        await self.accept()


        order_data = await self.get_order_data(self.outlet)
        await self.send(text_data=json.dumps({'message': order_data}))
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == 'all_orders':
            order_data = await self.get_order_data(self.outlet)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': order_data
            }
            )   
        if message == 'orderhistory':
            order_data = await self.get_orderhistory_data(self.outlet)
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': order_data
            }
            ) 

    async def chat_message(self, event):
        print("I came here")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


    from channels.db import database_sync_to_async


    # Convert max_prep_time to "HH:MM:SS" format for the output
    def seconds_to_hhmmss(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"


    @database_sync_to_async
    def get_order_data(self, outlet):
        order_dict = {
            "products": [],  # Initialize as an empty list
            "counts": {}
        }

        # Group OrderDetails by botID
        from collections import defaultdict
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
        from bill.models import tblOrderTracker
        from django.db.models import Q
        from datetime import datetime

        # Fetch relevant order details
        for order_details in tblOrderTracker.objects.filter(
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=self.outlet)
        ).order_by('-id'):
            bot_id = order_details.botID if order_details.botID else "undefined"
            order_detailId = order_details.id 
            itemName = order_details.product.title if order_details.product else ""
            modification = order_details.modification if order_details.modification else ""
            quantity = order_details.product_quantity if order_details.product_quantity else 0
            product_id = order_details.product.id if order_details.product else ""  
            order_type = order_details.order.order_type if order_details.order.order_type else ""
            order_id = order_details.order.id 
            table_no = order_details.order.table_no if order_details.order.table_no else ""
            date_time_str = order_details.ordertime if order_details.ordertime else ""
            
            # Handle dateTime formatting
            dateTime = ""
            if date_time_str:
                datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
                dateTime = datetime_obj.strftime("%H:%M:%S")

            employee = order_details.order.employee if order_details.order.employee else ""
            noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else 0
            customer = order_details.order.customer.name if order_details.order.customer else ""              
            seen = order_details.seen 
            branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
            terminal = order_details.order.terminal_no if order_details.order else ""                
            state = order_details.state if order_details.state else ""           

            # Prepare item dictionary
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
                'branch': branch,
                'terminal': terminal,
                'state': state
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

        # Build the final order_dict
        for bot_id, items in bot_groups.items():
            order_dict["products"].append({
                "kot_id": bot_id,
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
                "max_prep_time": self.seconds_to_hhmmss(items['max_prep_time'])
            })

        order_dict['type'] = 'orders'
        from django.db.models import Sum, Q
        from django.utils import timezone

        # Get today's date
        today = timezone.now().date()

        not_seen = tblOrderTracker.objects.filter(
            Q(seen=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
        cooking = tblOrderTracker.objects.filter(
            Q(seen=True),
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
    
        cooked = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).count()
        from django.db.models import Sum
        total_void_quantity = tblOrderTracker.objects.filter(
            Q(state='Void'), 
            Q(order__branch__branch_code=outlet),
            Q(product__print_display='BAR'),
            Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
            ).aggregate(total_quantity=Sum('product_quantity'))    

        order_dict['counts']['not_seen'] = not_seen
        order_dict['counts']['cooking'] = cooking
        order_dict['counts']['cooked'] = cooked
        order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

        order_dict['counts']['total_order_today'] = len(order_dict['products'])

        return order_dict
    
    @database_sync_to_async
    def get_orderhistory_data(self, outlet):
        # order_dict = {
        #     "products": [],  # Initialize as an empty list
        #     "counts": {}
        # }
        final_dict={
            "type": "orderhistory",
            "data":{
                "completed": [],
                "preparing": []
            }
        }
        # Group OrderDetails by kotID
        from collections import defaultdict
        from bill.models import tblOrderTracker
        from django.db.models import Q
        from datetime import datetime


        # Fetch relevant order details
        from django.db.models import Sum, F

        # Fetch relevant order details
        order_details_queryset_preparing = tblOrderTracker.objects.filter(
            Q(done=False),
            ~Q(botID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).annotate(
            product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
            product_rate=F('rate'),
            product_group=F('product__group')  # Add this line to get the product group
        ).values(
            'product_title', 'product_rate', 'product_group'
        ).annotate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum(F('rate') * F('product_quantity'))
        ).order_by('-total_quantity')  # Order by total quantity if needed

        # Convert to a list of dictionaries
        result = [
            {
                'product_title': entry['product_title'],
                'product_rate': float(entry['product_rate']),
                'product_group': entry['product_group'],  # Include product group
                'total_quantity': float(entry['total_quantity']),
                'total_amount': float(entry['total_amount'])
            }
            for entry in order_details_queryset_preparing
        ]

        for item_dict in order_details_queryset_preparing:
        # Build the final order_dict
            final_dict["data"]["preparing"].append(
                {
                    'product_title': item_dict['product_title'],
                    'product_rate': float(item_dict['product_rate']),
                    'product_group': item_dict['product_group'],  # Include product group
                    'total_quantity': float(item_dict['total_quantity']),
                    'total_amount': float(item_dict['total_amount'])
                }
            )
        # Fetch relevant order details
        order_details_queryset_completed = tblOrderTracker.objects.filter(
            Q(done=True),
            ~Q(kotID=None),
            Q(product__print_display='BAR'),
            Q(product_quantity__gt=0),
            Q(order__branch__branch_code=outlet)
        ).annotate(
            product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
            product_rate=F('rate'),
            product_group=F('product__group')  # Add this line to get the product group
        ).values(
            'product_title', 'product_rate', 'product_group'
        ).annotate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum(F('rate') * F('product_quantity'))
        ).order_by('-total_quantity')  # Order by total quantity if needed

        # Convert to a list of dictionaries
        result = [
            {
                'product_title': entry['product_title'],
                'product_rate': float(entry['product_rate']),
                'product_group': entry['product_group'],  # Include product group
                'total_quantity': float(entry['total_quantity']),
                'total_amount': float(entry['total_amount'])
            }
            for entry in order_details_queryset_completed
        ]

        print(f'order_details_queryset_completed  {order_details_queryset_completed}')
        for item_dict in order_details_queryset_completed:
        # Build the final order_dict
            final_dict["data"]["completed"].append(
                {
                    'product_title': item_dict['product_title'],
                    'product_rate': float(item_dict['product_rate']),
                    'product_group': item_dict['product_group'],  # Include product group
                    'total_quantity': float(item_dict['total_quantity']),
                    'total_amount': float(item_dict['total_amount'])
                }
            )

        return final_dict


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# class BarConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Extract the outlet from the query parameters
#         self.outlet = self.scope['query_string'].decode('utf-8').split('=')[1]  # Assumes the format is `outlet=your_outlet`

#         # Create a dynamic group name based on the outlet
#         # self.group_name = f"chat_group_{self.outlet}"

#         self.group_name = f"bar_group_{self.outlet}"
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         order_data = await self.get_order_data(self.outlet)
#         await self.send(text_data=json.dumps({'message': order_data}))
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         if message == 'all_orders':
#             order_data = await self.get_order_data(self.outlet)
#             await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': order_data
#             }
#             ) 
#         if message == 'orderhistory':
#             order_data = await self.get_orderhistory_data(self.outlet)
#             await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': order_data
#             }
#             )   
#         # if message == 'orderhistory':
#         #     order_data = await self.get_order_data()
#         #     await self.channel_layer.group_send(
#         #     self.group_name,
#         #     {
#         #         'type': 'chat_message',
#         #         'message': order_data
#         #     }
#         #     ) 
#         # await self.channel_layer.group_send(
#         #     self.group_name,
#         #     {
#         #         'type': 'chat_message',
#         #         'message': message
#         #     }
#         # )
#     async def chat_message(self, event):
#         print("I came here")
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     # from channels.db import database_sync_to_async
#     # @database_sync_to_async
#     # def get_order_data(self):
#     #     order_dict = {
#     #         "products": []  # Initialize as an empty list
#     #     }

#     #     # Group OrderDetails by kotID
#     #     from collections import defaultdict

#     #     kot_groups = defaultdict(lambda: {"details": [], "void_items": []})  

#     #     from bill.models import OrderDetails, tblOrderTracker
#     #     from django.db.models import Q
#     #     for order_details in tblOrderTracker.objects.filter(Q(done=False), ~Q(kotID=None), Q(product__print_display='BAR'),Q(product_quantity__gt=0)).order_by('-id'):
#     #         kot_id = order_details.kotID if order_details.kotID else "undefined"
#     #         order_detailId = order_details.id 
#     #         itemName = order_details.product.title if order_details.product else ""
#     #         modification = order_details.modification if order_details.modification else ""
#     #         quantity = order_details.product_quantity if order_details.product_quantity else 0
#     #         product_id = order_details.product.id if order_details.product else ""
#     #         order_type = order_details.order.order_type if order_details.order.order_type else ""
#     #         order_id = order_details.order.id 
#     #         table_no = order_details.order.table_no if order_details.order.table_no else ""
#     #         date_time_str = order_details.ordertime if order_details.ordertime else ""
#     #         from datetime import datetime
#     #         if date_time_str:
#     #             # Parse the string into a datetime object
#     #             datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
                
#     #             # Convert it to the desired format
#     #             dateTime = datetime_obj.strftime("%H:%M: %S")
#     #         else:
#     #             dateTime = ""
#     #         employee = order_details.order.employee if order_details.order.employee else ""
#     #         noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else ""
#     #         customer = order_details.order.customer.name if order_details.order.customer else ""              
#     #         seen = order_details.seen             
#     #         branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
#     #         terminal = order_details.order.terminal_no if order_details.order else ""   
#     #         state = order_details.state if order_details.state else ""
#     #         # kot_groups[kot_id].append({
#     #         #     'orderdetailId': order_detailId,
#     #         #     'itemName': itemName,
#     #         #     'modification': modification,
#     #         #     'quantity': quantity,
#     #         #     'product_id': product_id,
#     #         #     'kot_id': str(kot_id),
#     #         #     'order_type': str(order_type),
#     #         #     'order_id': order_id,
#     #         #     'table_no': str(table_no),
#     #         #     'dateTime': str(dateTime),
#     #         #     'employee': employee,
#     #         #     'noOfGuest': int(noOfGuest),
#     #         #     'customer': customer,
#     #         #     'seen':seen,
#     #         #     'branch' : branch ,             
#     #         #     'terminal' :terminal,
#     #         #     'state': state
#     #         # })
#     #         item_dict = {
#     #             'orderdetailId': order_detailId,
#     #             'itemName': itemName,
#     #             'modification': modification,
#     #             'quantity': quantity,
#     #             'product_id': product_id,
#     #             'kot_id': str(kot_id),
#     #             'order_type': str(order_type),
#     #             'order_id': order_id,
#     #             'table_no': str(table_no),
#     #             'dateTime': str(dateTime),
#     #             'employee': employee,
#     #             'noOfGuest': noOfGuest,
#     #             'customer': customer,
#     #             'seen': seen,
#     #             'branch' : branch ,             
#     #             'terminal' :terminal,
#     #             'state':state
#     #         }

#     #         if state == "Normal":
#     #             kot_groups[kot_id]["details"].append(item_dict)
#     #         elif state == "Void":
#     #             kot_groups[kot_id]["void_items"].append(item_dict)

#     #     for kot_id, items in kot_groups.items():
#     #         order_dict["products"].append({
#     #             "kot_id": kot_id,
#     #             'dateTime': str(dateTime),
#     #             'seen': seen,
#     #             'state':state,
#     #             'employee': employee,
#     #             'order_type': str(order_type),
#     #             'noOfGuest': noOfGuest,
#     #             'customer': customer,
#     #             'table_no': str(table_no),

#     #             'order_id': order_id,
#     #             "details": items["details"],
#     #             "void_items": items["void_items"]
#     #         })

#     #     # for kot_id, details in kot_groups.items():
#     #     #     order_dict["products"].append({
#     #     #         "kot_id": kot_id,
#     #     #         "details": details
#     #     #     })

#     #     order_dict['type'] = 'orders'
#     #     return order_dict

#     from channels.db import database_sync_to_async



#     @database_sync_to_async
#     def get_order_data(self, outlet):
#         order_dict = {
#             "products": [],  # Initialize as an empty list
#             "counts": {}
#         }

#         # Group OrderDetails by kotID
#         from collections import defaultdict
#         bot_groups = defaultdict(lambda: {
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
#         from bill.models import tblOrderTracker
#         from django.db.models import Q
#         from datetime import datetime

#         # Fetch relevant order details
#         for order_details in tblOrderTracker.objects.filter(
#             Q(done=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).order_by('-id'):
#             bot_id = order_details.botID if order_details.botID else "undefined"
#             order_detailId = order_details.id 
#             itemName = order_details.product.title if order_details.product else ""
#             modification = order_details.modification if order_details.modification else ""
#             quantity = order_details.product_quantity if order_details.product_quantity else 0
#             product_id = order_details.product.id if order_details.product else ""  
#             order_type = order_details.order.order_type if order_details.order.order_type else ""
#             order_id = order_details.order.id 
#             table_no = order_details.order.table_no if order_details.order.table_no else ""
#             date_time_str = order_details.ordertime if order_details.ordertime else ""
            
#             # Handle dateTime formatting
#             dateTime = ""
#             if date_time_str:
#                 datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %I:%M:%S %p")
#                 dateTime = datetime_obj.strftime("%H:%M:%S")

#             employee = order_details.order.employee if order_details.order.employee else ""
#             noOfGuest = order_details.order.no_of_guest if order_details.order.no_of_guest else 0
#             customer = order_details.order.customer.name if order_details.order.customer else ""              
#             seen = order_details.seen 
#             branch = order_details.order.branch.branch_code if order_details.order.branch else ""              
#             terminal = order_details.order.terminal_no if order_details.order else ""                
#             state = order_details.state if order_details.state else ""           

#             # Prepare item dictionary
#             item_dict = {
#                 'orderdetailId': order_detailId,
#                 'itemName': itemName,
#                 'modification': modification,
#                 'quantity': quantity,
#                 'product_id': product_id,
#                 'bot_id': str(bot_id),
#                 'order_type': str(order_type),
#                 'order_id': order_id,
#                 'table_no': str(table_no),
#                 'dateTime': str(dateTime),
#                 'employee': employee,
#                 'noOfGuest': noOfGuest,
#                 'customer': customer,
#                 'seen': seen,
#                 'branch': branch,
#                 'terminal': terminal,
#                 'state': state
#             }

#             # Group details and void items
#             bot_info = bot_groups[bot_id]
#             bot_info['dateTime'] = dateTime
#             bot_info['seen'] = seen
#             bot_info['state'] = state
#             bot_info['employee'] = employee
#             bot_info['order_type'] = order_type
#             bot_info['noOfGuest'] = noOfGuest
#             bot_info['table_no'] = str(table_no)
#             bot_info['customer'] = customer
#             bot_info['order_id'] = order_id

#             if state == "Normal":
#                 bot_info["details"].append(item_dict)
#             elif state == "Void":
#                 bot_info["void_items"].append(item_dict)

#         # Build the final order_dict
#         for bot_id, items in bot_groups.items():
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

#         order_dict['type'] = 'orders'
#         from django.db.models import Sum, Q
#         from django.db.models.functions import TruncDate
#         from django.utils import timezone

#         # Get today's date
#         today = timezone.now().date()

#         not_seen = tblOrderTracker.objects.filter(
#             Q(seen=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).count()
#         cooking = tblOrderTracker.objects.filter(
#             Q(seen=True),
#             Q(done=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).count()
    
#         cooked = tblOrderTracker.objects.filter(
#             Q(done=True),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).count()
#         from django.db.models import Sum
#         total_void_quantity = tblOrderTracker.objects.filter(
#             Q(state='Void'), 
#             Q(order__branch__branch_code=outlet),
#             Q(product__print_display='BAR'),
#             Q(ordertime__startswith=today.strftime('%Y-%m-%d'))
#             ).aggregate(total_quantity=Sum('product_quantity'))    

#         order_dict['counts']['not_seen'] = not_seen
#         order_dict['counts']['cooking'] = cooking
#         order_dict['counts']['cooked'] = cooked
#         order_dict['counts']['total_void_quantity'] = total_void_quantity["total_quantity"] if total_void_quantity["total_quantity"] else 0

#         order_dict['counts']['total_order_today'] = len(order_dict['products'])
#         return order_dict
    
#     @database_sync_to_async
#     def get_orderhistory_data(self, outlet):
#         # order_dict = {
#         #     "products": [],  # Initialize as an empty list
#         #     "counts": {}
#         # }
#         final_dict={
#             "type": "orderhistory",
#             "data":{
#                 "completed": [],
#                 "preparing": []
#             }
#         }
#         # Group OrderDetails by kotID
#         from collections import defaultdict
#         from bill.models import tblOrderTracker
#         from django.db.models import Q
#         from datetime import datetime


#         # Fetch relevant order details
#         from django.db.models import Sum, F

#         # Fetch relevant order details
#         order_details_queryset_preparing = tblOrderTracker.objects.filter(
#             Q(done=False),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).annotate(
#             product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
#             product_rate=F('rate'),
#             product_group=F('product__group')  # Add this line to get the product group
#         ).values(
#             'product_title', 'product_rate', 'product_group'
#         ).annotate(
#             total_quantity=Sum('product_quantity'),
#             total_amount=Sum(F('rate') * F('product_quantity'))
#         ).order_by('-total_quantity')  # Order by total quantity if needed

#         # Convert to a list of dictionaries
#         result = [
#             {
#                 'product_title': entry['product_title'],
#                 'product_rate': float(entry['product_rate']),
#                 'product_group': entry['product_group'],  # Include product group
#                 'total_quantity': float(entry['total_quantity']),
#                 'total_amount': float(entry['total_amount'])
#             }
#             for entry in order_details_queryset_preparing
#         ]

#         for item_dict in order_details_queryset_preparing:
#         # Build the final order_dict
#             final_dict["data"]["preparing"].append(
#                 {
#                     'product_title': item_dict['product_title'],
#                     'product_rate': float(item_dict['product_rate']),
#                     'product_group': item_dict['product_group'],  # Include product group
#                     'total_quantity': float(item_dict['total_quantity']),
#                     'total_amount': float(item_dict['total_amount'])
#                 }
#             )
#         # Fetch relevant order details
#         order_details_queryset_completed = tblOrderTracker.objects.filter(
#             Q(done=True),
#             ~Q(botID=None),
#             Q(product__print_display='BAR'),
#             Q(product_quantity__gt=0),
#             Q(order__branch__branch_code=outlet)
#         ).annotate(
#             product_title=F('product__title'),  # Assuming 'title' is the field name in Product model
#             product_rate=F('rate'),
#             product_group=F('product__group')  # Add this line to get the product group
#         ).values(
#             'product_title', 'product_rate', 'product_group'
#         ).annotate(
#             total_quantity=Sum('product_quantity'),
#             total_amount=Sum(F('rate') * F('product_quantity'))
#         ).order_by('-total_quantity')  # Order by total quantity if needed

#         # Convert to a list of dictionaries
#         result = [
#             {
#                 'product_title': entry['product_title'],
#                 'product_rate': float(entry['product_rate']),
#                 'product_group': entry['product_group'],  # Include product group
#                 'total_quantity': float(entry['total_quantity']),
#                 'total_amount': float(entry['total_amount'])
#             }
#             for entry in order_details_queryset_completed
#         ]

#         print(f'order_details_queryset_completed  {order_details_queryset_completed}')
#         for item_dict in order_details_queryset_completed:
#         # Build the final order_dict 
#             final_dict["data"]["completed"].append(
#                 {
#                     'product_title': item_dict['product_title'],
#                     'product_rate': float(item_dict['product_rate']),
#                     'product_group': item_dict['product_group'],  # Include product group
#                     'total_quantity': float(item_dict['total_quantity']),
#                     'total_amount': float(item_dict['total_amount'])
#                 }
#             )

#         return final_dict