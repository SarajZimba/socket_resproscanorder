
from django.db.models import Sum, Max
from bill.models import Bill, MobilePaymentSummary
from bill.models import MobilePaymentType, BillPayment  # Adjust the import based on your project structure

def get_payment_modes_summary_todays_sales(queryset):
    # Filter bills that are after the latest_created_date
    bills = queryset

    # Get the IDs of the bills
    bill_ids = bills.values_list('id', flat=True)

    # Group BillPayment by payment_mode and sum the 'amount'
    payment_mode_summary = (
        BillPayment.objects
        .filter(bill_id__in=bill_ids)
        .values('payment_mode')  # Group by payment_mode
        .annotate(total_amount=Sum('amount'))  # Sum the amount for each payment_mode
    )

    # Format the result
    results = []
    for item in payment_mode_summary:
        results.append({
            'payment_mode': item['payment_mode'],
            'total_amount': item['total_amount']
        })

    return results


from collections import defaultdict
from django.db.models import Max
from .models import EndDayDailyReport

def get_complementary_bills_todays_sales(queryset):


    from bill.models import Bill
    
    # Get complimentary bills after the latest_created_date
    complimentary_bills = queryset.filter(
        payment_mode="COMPLIMENTARY",
    ).select_related('customer').prefetch_related('bill_items__product')

    # Get aggregated bill items customer-wise
    complimentary_bill_items = calculate_bill_items_total(complimentary_bills)

    print("complimentary_bill_items", complimentary_bill_items)
    return complimentary_bill_items  # Return the customer-wise aggregated items


def calculate_bill_items_total(queryset):
    # Dictionary to store totals per customer
    customer_bill_items_total = defaultdict(lambda: defaultdict(list))

    # Dictionary to store product quantities (grouped by product_id, rate)
    product_quantities = defaultdict(lambda: {'quantity': 0, 'rate': 0, 'product_title': '', 'type': '', 'customer': None})

    for bill in queryset:
        customer_id = bill.customer.id  # Use customer ID or customer_name if preferred
        customer_name = bill.customer_name  # Optional: use customer_name if customer ID isn't available
        
        for bill_item in bill.bill_items.all():
            product_id = bill_item.product.id
            quantity = bill_item.product_quantity
            rate = bill_item.rate
            product_title = bill_item.product_title
            product_category = bill_item.product.type.title  # Assuming 'type' is the related field to ProductCategory

            key = (customer_id, product_id, rate)

            # Aggregate product quantities for the same customer, product, and rate
            if key in product_quantities:
                product_quantities[key]['quantity'] += quantity
            else:
                product_quantities[key] = {
                    'quantity': quantity,
                    'rate': rate,
                    'product_title': product_title,
                    'type': product_category,
                    'customer': customer_id  # You could also store customer_name here if needed
                }

    # Organize data customer-wise
    for (customer_id, product_id, rate), item_data in product_quantities.items():
        customer_bill_items_total[item_data['customer']][item_data['type']].append({
            'product_title': item_data['product_title'],
            'product_quantity': item_data['quantity'],
            'rate': item_data['rate'],
            'amount': item_data['quantity'] * item_data['rate'],
            'customer': customer_id,  # This can be customer_name if preferred
            # 'customer_name': customer_name
        })

    # Convert defaultdict to the desired format: [{customer: 33, items: [...]}, ...]
    result = []
    for customer, items_by_category in customer_bill_items_total.items():
        # Flatten the items grouped by category into a single list of items
        all_items = []
        total_amount = 0  # Initialize total amount for this customer
        for items in items_by_category.values():
            all_items.extend(items)  # Merge all category items into one list
            total_amount += sum(item['amount'] for item in items)
        from user.models import Customer
        result.append({
            'customer': customer,
            'customer_name':Customer.objects.get(id=customer).name,
            'items': all_items,
            'total': total_amount  # Include the total amount for the customer
        })

    return result  # Return the final list of dictionaries with customer and items


from django.db.models import Sum, Max
from bill.models import Bill, MobilePaymentSummary
from bill.models import MobilePaymentType  # Adjust the import based on your project structure

def get_mobile_payments_todays_sales(queryset):

    # Get complimentary bills after the latest_created_date
    bills = queryset.filter(
        payment_mode="MOBILE PAYMENT"
    )

    # Get the IDs of the bills retrieved
    bill_ids = bills.values_list('id', flat=True)

    # Calculate the sum of MobilePaymentSummary values grouped by payment type
    mobile_payment_summary = (
        MobilePaymentSummary.objects
        .filter(bill_id__in=bill_ids)
        .values('type')  # Get the payment type ID
        .annotate(total_amount=Sum('value'))  # Sum the 'value' field
    )

    # Now join with MobilePaymentType to get the name
    results = []
    for item in mobile_payment_summary:
        payment_type = MobilePaymentType.objects.get(id=item['type'])
        results.append({
            'type': payment_type.id,
            'name': payment_type.name,
            'total_amount': item['total_amount']
        })

    return results