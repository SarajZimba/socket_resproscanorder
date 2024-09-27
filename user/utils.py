from .models import Customer
def check_email(email):
    if Customer.objects.filter(email=email, type='Normal').exists():
        return True #means already email associated with another account
    else:
        return False 
    
def check_phone(phone):
    if Customer.objects.filter(phone=phone, type='Normal').exists():
        return True #means already email associated with another account
    else:
        return False 
        
def check_email_in_normal(email):
    if Customer.objects.filter(email=email, type='Google').exists():
        return True #means already email associated with another account
    else:
        return False 
    
from django.db.models import Q
from decimal import Decimal 
from menu.models import TblRedeemedProduct
def check_points_availability(customer, api_points, order):
    customer_points = customer.loyalty_points
    existing_redeemedproducts = TblRedeemedProduct.objects.filter(~Q(state='Completed'), customer=customer, order=order)

    total_poinsForexistingredeemedproducts = 0
    for item in existing_redeemedproducts:
        total_poinsForexistingredeemedproducts += item.redeemproduct.points
    total_redeemedproductsPointsin_tbl = total_poinsForexistingredeemedproducts + api_points
    if total_redeemedproductsPointsin_tbl <= customer_points:
        flag = True
    else:
        flag = False

    return flag

def get_customer_points_after_redeemed(customer, redeemed_points):

    current_points = customer.loyalty_points
    new_points = current_points - Decimal(redeemed_points)

    return new_points
    
    
from django.db.models import Sum
from order.models import ScanPayOrder, ScanPayOrderDetails
from bill.models import Order, OrderDetails
from organization.models import Terminal, Table
def reduce_redeemedproducts_from_normalandscanpay(order):


    tblredeemedproducts = (TblRedeemedProduct.objects.filter(
        order__id = int(order), redeemproduct__is_Menuitem=True)
    .values('redeemproduct__MenuitemID__item_name')  # Group by the redeemproduct
    .annotate(total_quantity=Sum('quantity'))  # Sum the quantities)
    )   
    scanpayorder = ScanPayOrder.objects.get(pk=int(order))
    scanpayorderdetails = ScanPayOrderDetails.objects.filter(order=scanpayorder)

    tblredeemedproducts_for_normal = tblredeemedproducts
    normal_orderid = scanpayorder.outlet_order
    normalorder = Order.objects.get(pk=int(normal_orderid))
    normalorderdetails = OrderDetails.objects.filter(order=normalorder)


    for redeemedproducts in tblredeemedproducts:
        redeemed_quantity  =  redeemedproducts['total_quantity']
        for orderdetails in scanpayorderdetails:
            if orderdetails.itemName == redeemedproducts['redeemproduct__MenuitemID__item_name']:
                if orderdetails.quantity <= redeemed_quantity:
                    redeemed_quantity -= orderdetails.quantity
                    orderdetails.delete()
                else:
                    orderdetails.quantity -= redeemed_quantity

                    orderdetails.save()
                    redeemed_quantity = 0
                    break

        if redeemed_quantity == 0:
            break  # Exit the outer loop if the redeemed quantity is fully used
    # delete the order if all orderdetails are deleted
    check_scanpayorderdetails = ScanPayOrderDetails.objects.filter(order=scanpayorder).exists()

    if check_scanpayorderdetails == False:
         scanpayorder.delete()

    for redeemedproducts in tblredeemedproducts_for_normal:
        redeemed_quantity  =  redeemedproducts['total_quantity']
        for orderdetails in normalorderdetails:
            if orderdetails.product.title == redeemedproducts['redeemproduct__MenuitemID__item_name']:
                if orderdetails.product_quantity <= redeemed_quantity:
                    redeemed_quantity -= orderdetails.product_quantity
                    orderdetails.delete()
                else:
                    orderdetails.product_quantity -= redeemed_quantity

                    orderdetails.save()
                    redeemed_quantity = 0
                    break

        if redeemed_quantity == 0:
            break  # Exit the outer loop if the redeemed quantity is fully used
        # cancel order if orderdetails are deleted
    check_normalorderdetails = OrderDetails.objects.filter(order=normalorder).exists()

    if check_normalorderdetails == False:
            table_no = normalorder.table_no
            terminal_no = normalorder.terminal_no
            branch = normalorder.branch
            table = Table.objects.get(terminal=Terminal.objects.get(terminal_no=terminal_no, branch=branch, is_deleted=False, status=True), table_number=table_no)
            table.is_estimated = False
            table.is_occupied = False
            table.save()
            normalorder.status=False
            normalorder.save()
    