from rest_framework.response import Response
from rest_framework.views import APIView
from bill.models import VoidBillTracker, Bill, TablReturnEntry, Order, OrderDetails, BillItemVoid
from rest_framework import status
from product.models import Product
from organization.models import Table, Terminal


class MakeVoidBill(APIView):

    def post(self, request, order_id, format=None):
        data = request.data

        reason = data.get("voidReason")
        bill = Bill.objects.get(order__id=order_id)
        bill_id = bill.id
        voidbillobj = VoidBillTracker.objects.create(prev_bill=bill.invoice_number, prev_bill_id=bill_id, bill_prev=bill)

        # bill = Bill.objects.get(invoice_number=biinvoice_number, fiscal_year=fiscal_year)
        bill.status = False
        bill.save()

        miti = bill.transaction_miti
        quantity = bill.bill_items.count()
        return_entry = TablReturnEntry(
            bill_date=bill.transaction_date,
            bill_no=bill.invoice_number,
            customer_name=bill.customer_name,
            customer_pan=bill.customer_tax_number,
            amount=bill.grand_total,
            NoTaxSales=0,
            ZeroTaxSales=0,
            taxable_amount=bill.taxable_amount,
            tax_amount=bill.tax_amount,
            miti=miti,
            ServicedItem="Goods",
            quantity=quantity,
            reason=reason,
            fiscal_year=bill.fiscal_year
        )
        try:
            return_entry.save()
        except Exception as e:
            print(e)

        voidbillobj_id = voidbillobj.id
        return Response({"voidbillobj_id": voidbillobj_id}, status=status.HTTP_201_CREATED)
  
# from bill.models import FutureOrder, FutureOrderDetails        
# class VoidBillItemView(APIView):

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         void_item = data.get('void_item')
#         orderdetails_items = data.get('orderdetails_items')
#         order = data.get('order')
#         try:
#             order_obj = Order.objects.get(id=order)
#         except Order.DoesNotExist:
#             return Response({"error": f"Order with ID {order} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             futureorder_obj = FutureOrder.objects.get(order=order_obj)
#         except FutureOrder.DoesNotExist:
#             return Response({"error": f"Future Order with ID {order} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

#         OrderDetails.objects.filter(order=order_obj).delete()
#         FutureOrderDetails.objects.filter(order=futureorder_obj).delete()
#         if orderdetails_items == []:
#             # order = Order.objects.get(id=order)
#             table_no = order_obj.table_no
#             terminal_no = order_obj.terminal_no
#             branch = order_obj.branch
#             table = Table.objects.get(terminal=Terminal.objects.get(terminal_no=terminal_no, branch=branch, is_deleted=False, status=True), table_number=table_no)
#             table.is_estimated = False
#             table.is_occupied = False
#             table.save()
#             order_obj.status=False
#             order_obj.save()
#         else:

#             for item in orderdetails_items:
    
#                 product = item['product']
#                 product_quantity = item['product_quantity']
#                 kotID = item['kotID']
#                 botID = item['botID']
#                 modification = item['modification']
#                 ordertime = item['ordertime']
#                 employee = item['employee']
    
    
#                 order_item = OrderDetails.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=product_quantity, kotID=kotID, botID=botID, modification=modification, ordertime=ordertime, employee=employee)
#                 futureorder_item = FutureOrderDetails.objects.create(order=futureorder_obj, product=Product.objects.get(id=product), product_quantity=product_quantity, kotID=kotID, botID=botID, modification=modification, ordertime=ordertime, employee=employee)


#         # for void_item in void_items:

#         qty = void_item['quantity']
#         product = void_item['product']
#         count = void_item['count']
#         isBefore = void_item['isBefore']
#         reason = void_item['reason']
#         BillItemVoid.objects.create(quantity=qty, product=Product.objects.get(id=product), count=count, isBefore=isBefore, order=order_obj, reason=reason)

#         return Response("VoidItems Created Successfully", status=status.HTTP_200_OK)


from order.models import ScanPayOrder, ScanPayOrderDetails
from order.utils import send_bar_order_notification_socket, send_order_notification_socket
from bill.models import FutureOrder, FutureOrderDetails, tblOrderTracker  
from django.db.models import Q       
class VoidBillItemView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        void_item = data.get('void_item')
        orderdetails_items = data.get('orderdetails_items')
        order = data.get('order')
        try:
            order_obj = Order.objects.get(id=order)
        except Order.DoesNotExist:
            return Response({"error": f"Order with ID {order} does not exist."}, status=status.HTTP_400_BAD_REQUEST)


        futureorder_obj = FutureOrder.objects.filter(order=order_obj).first()

        if futureorder_obj:
            FutureOrderDetails.objects.filter(order=futureorder_obj).delete()
            if orderdetails_items == []:
                futureorder_obj.status=False
                futureorder_obj.save()
            else:

                for item in orderdetails_items:
        
                    product = item['product']
                    product_quantity = item['product_quantity']
                    kotID = item['kotID']
                    botID = item['botID']
                    modification = item['modification']
                    ordertime = item['ordertime']
                    employee = item['employee']
                    rate = item['rate']
        
                    futureorder_item = FutureOrderDetails.objects.create(order=futureorder_obj, product=Product.objects.get(id=product), product_quantity=product_quantity, kotID=kotID, botID=botID, modification=modification, ordertime=ordertime, employee=employee, rate=rate)


        
        scanpayorder_obj = ScanPayOrder.objects.filter(outlet_order=order_obj.id).first()

        if scanpayorder_obj:
            ScanPayOrderDetails.objects.filter(order=scanpayorder_obj).delete()
            if orderdetails_items == []:
                scanpayorder_obj.status=False
                scanpayorder_obj.save()
            else:

                for item in orderdetails_items:
        
                    product = item['product']
                    product_quantity = item['product_quantity']
                    kotID = item['kotID']
                    botID = item['botID']
                    modification = item['modification']
                    ordertime = item['ordertime']
                    employee = item['employee']
                    rate = item['rate']

                    scanpayorder_item = ScanPayOrderDetails.objects.create(order=scanpayorder_obj, itemName=Product.objects.get(id=product).title, quantity=product_quantity, modification=modification, total=rate*product_quantity, rate=rate)

        OrderDetails.objects.filter(order=order_obj).delete()
        if orderdetails_items == []:
            # order = Order.objects.get(id=order)
            table_no = order_obj.table_no
            terminal_no = order_obj.terminal_no
            branch = order_obj.branch
            table = Table.objects.get(terminal=Terminal.objects.get(terminal_no=terminal_no, branch=branch, is_deleted=False, status=True), table_number=table_no)
            table.is_estimated = False
            table.is_occupied = False
            table.save()
            order_obj.status=False
            order_obj.save()
        else:

            for item in orderdetails_items:
    
                product = item['product']
                product_quantity = item['product_quantity']
                kotID = item['kotID']
                botID = item['botID']
                modification = item['modification']
                ordertime = item['ordertime']
                employee = item['employee']
                rate = item['rate']

    
                order_item = OrderDetails.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=product_quantity, kotID=kotID, botID=botID, modification=modification, ordertime=ordertime, employee=employee, rate=rate)

        qty = void_item['quantity']
        product = void_item['product']
        count = void_item['count']
        isBefore = void_item['isBefore']
        reason = void_item['reason']
        void_kot = void_item['kotId']
        void_bot = void_item['botId']
        employee = void_item['employee']
        print(f"kot {void_kot}")
        print(f"bot {void_bot}")
        print(f"void_qty {qty}")
        BillItemVoid.objects.create(quantity=qty, product=Product.objects.get(id=product), count=count, isBefore=isBefore, order=order_obj, reason=reason, employee=employee)
        total_quantity_ordertracker = 0
        existing_ordertrackers = tblOrderTracker.objects.filter(order=order_obj, product=Product.objects.get(id=product))
        for existing_ordertracker in existing_ordertrackers:
            total_quantity_ordertracker += existing_ordertracker.product_quantity
        existing_ordertrackers_notcompleted = tblOrderTracker.objects.filter(order=order_obj, product=Product.objects.get(id=product), is_completed=False, state='Normal')
        void_quantity = qty
        if existing_ordertrackers_notcompleted.exists():
            for ordertracker in existing_ordertrackers_notcompleted:

                if void_quantity > 0:
                    
                    if ordertracker.product_quantity <= void_quantity:
                        tblOrderTracker.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=ordertracker.product_quantity, kotID=ordertracker.kotID, botID=ordertracker.botID, done=ordertracker.done, seen=ordertracker.seen, state='Void', is_completed=ordertracker.is_completed, ordertime=ordertracker.ordertime, reason=reason)
                        # total_quantity_ordertracker -= ordertracker.quantity
                        void_quantity -= ordertracker.product_quantity
                        ordertracker.product_quantity = 0

                        ordertracker.delete()


                    else:
                        ordertracker.product_quantity -= void_quantity
                        # total_quantity_ordertracker -= void_quantity

                        tblOrderTracker.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=void_quantity, kotID=ordertracker.kotID, botID=ordertracker.botID, state='Void',is_completed=ordertracker.is_completed, done=ordertracker.done, seen=ordertracker.seen, ordertime=ordertracker.ordertime, reason=reason)
                        ordertracker.save()
                        void_quantity = 0
                        break
                else:
                    break

        if void_quantity != 0:
            completed_queryset = tblOrderTracker.objects.filter(order=order_obj, product=Product.objects.get(id=product), is_completed=True, state='Normal')
            if completed_queryset.exists():
                existing_ordertrackers_completed = tblOrderTracker.objects.filter(order=order_obj, product=Product.objects.get(id=product), is_completed=True, state='Normal')

                if existing_ordertrackers_completed:
                    for ordertracker in existing_ordertrackers_completed:

                        if void_quantity > 0:
                            
                            if ordertracker.product_quantity <= void_quantity:
                                tblOrderTracker.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=ordertracker.product_quantity, kotID=ordertracker.kotID, botID=ordertracker.botID, state='Void', is_completed=ordertracker.is_completed, done=ordertracker.done, seen=ordertracker.seen,ordertime=ordertracker.ordertime, reason=reason)
                                # total_quantity_ordertracker -= ordertracker.quantity
                                void_quantity -= ordertracker.product_quantity
                                ordertracker.product_quantity = 0
                                ordertracker.delete()


                            else:
                                ordertracker.product_quantity -= void_quantity
                                # total_quantity_ordertracker -= void_quantity
                                tblOrderTracker.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=void_quantity, kotID=ordertracker.kotID, botID=ordertracker.botID, state='Void',is_completed=ordertracker.is_completed, done=ordertracker.done, seen=ordertracker.seen,ordertime=ordertracker.ordertime, reason=reason)
                                ordertracker.save()
                                break
                        else:
                            break

        # tblOrderTracker.objects.create(order=order_obj, product=Product.objects.get(id=product), product_quantity=qty, kotID=void_kot, botID=void_bot, state='Void')
            # if order_obj.tblordertracker_set.filter(~Q(kotID=None)).exists():
            #     if not order_obj.tblordertracker_set.filter(~Q(botID=None)).exists():
            #         send_order_notification_socket(order_obj.branch.branch_code)
            # if order_obj.tblordertracker_set.filter(~Q(botID=None)).exists():

            #     if not order_obj.tblordertracker_set.filter(~Q(kotID=None) ).exists():
            #         send_bar_order_notification_socket(order_obj.branch.branch_code)
            # if order.tblordertracker_set.filter(~Q(botID=None)).exists():

            #     if  order_obj.tblordertracker_set.filter(~Q(kotID=None) ).exists():
            #         send_order_notification_socket(order_obj.branch.branch_code)
            #         send_bar_order_notification_socket(order_obj.branch.branch_code)
        if void_bot is not None:
            send_bar_order_notification_socket(order_obj.branch.branch_code)
        if void_kot is not None:
            send_order_notification_socket(order_obj.branch.branch_code)
     
        # send_order_notification_socket(order_obj.branch.branch_code)
        # send_bar_order_notification_socket(order_obj.branch.branch_code)
        return Response("VoidItems Created Successfully", status=status.HTTP_200_OK)
    


