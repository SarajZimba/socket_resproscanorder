from rest_framework import generics, status
from django.utils import timezone
from datetime import date
from api.serializers.end_day import EndDayDailyReportSerializer
from organization.models import EndDayDailyReport
from django.shortcuts import get_object_or_404
from organization.models import Branch, Terminal
from django.db.models import Q
from django.db.models import Sum
from organization.models import CashDrop
from django.db.models import Sum
from itertools import groupby
from operator import itemgetter
from organization.master_end_day import end_day
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from bill.models import Bill
from organization.utils import get_current_fiscal_year

class EndDayDailyReportFilterView(generics.ListAPIView):
    serializer_class = EndDayDailyReportSerializer

    def get_queryset(self):

        branch_id = self.kwargs.get('branch_id')
        branch = get_object_or_404(Branch, pk=branch_id)
        print(branch)
        # Get today's date
        today_date = date.today()
        today_date_str = today_date.strftime('%Y-%m-%d')

        # Filter records based on branch, terminal, and today's date
        queryset = EndDayDailyReport.objects.filter(
            Q(branch=branch)&
             Q(
            created_date__startswith=today_date_str)
        ).order_by('-date_time')  # Order by date_time in descending order to get the last entry

        return queryset
        
# from rest_framework.exceptions import APIException
# class MasterEndDay(APIView):
#     def get(self, request, *args, **kwargs):
#         jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
#         jwt_token = jwt_token.split()[1]
#         try:
#             token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
#             user_id = token_data.get("user_id")
#             username = token_data.get("username")
#             role = token_data.get("role")
#             # You can access other claims as needed

#             # Assuming "branch" is one of the claims, access it
#             branch = token_data.get("branch")

#             # Print the branch
#             print("Branch:", branch)
#         except jwt.ExpiredSignatureError:
#             print("Token has expired.")
#         except jwt.DecodeError:
#             print("Token is invalid.")
#         branch = Branch.objects.get(id=branch, is_deleted=False, status=True)
#         terminals = branch.terminal_set.filter(is_deleted=False, status=True)
#         daycloseForallterminal = True
#         for terminal in terminals:
#             if terminal.dayclose == False:
#                 daycloseForallterminal = False
#                 break
#             else:
#                 daycloseForallterminal=True
        
#         if daycloseForallterminal == True:
#             try:
#                 end_day()
#                 for terminal in terminals:
#                     terminal.dayclose = False
#                     terminal.save()
#             except Exception as e:
#                 print(e)
#                 return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             terminals = branch.terminal_set.filter(is_deleted=False, status=True, dayclose=False)
#             terminal_ids = []
#             for terminal in terminals:
#                 if terminal.dayclose == False:
#                     terminal_ids.append(terminal.terminal_no)
#             return Response({"detail": f"Terminal : {terminal_ids} need to close their days"}, status=status.HTTP_400_BAD_REQUEST)

        
        
#         return Response({"detail": "Endday has been done successfully"}, status=status.HTTP_200_OK)


from rest_framework.exceptions import APIException
class MasterEndDay(APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("name")
            role = token_data.get("role")
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")

            # Print the branch
            print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        branch = Branch.objects.get(id=branch, is_deleted=False, status=True)
        terminals = branch.terminal_set.filter(is_deleted=False, status=True)
        daycloseForallterminal = True
        # for terminal in terminals:
        #     if terminal.dayclose == False:
        #         daycloseForallterminal = False
        #         break
        #     else:
        #         daycloseForallterminal=True
        terminal_to_close_their_day = []
        for terminal in terminals:
            no_bill=True
            if Bill.objects.filter(is_end_day=False, status=True, terminal=terminal.terminal_no, branch=branch).exists():
                no_bill = False
            else:
                no_bill=True
            if (terminal.dayclose or no_bill) == False:
                daycloseForallterminal = False
                terminal_to_close_their_day.append(terminal.terminal_no)
                break
            else:
                daycloseForallterminal=True
        
        if daycloseForallterminal == True:
            try:
                branches = []
                branches.append(branch)
                end_day(branches, username)
                for terminal in terminals:
                    terminal.dayclose = False
                    terminal.save()
            except Exception as e:
                print(e)
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # terminals = branch.terminal_set.filter(is_deleted=False, status=True, dayclose=False)
            # terminal_ids = []
            # for terminal in terminal_to_close_their_day:
            #     if terminal.dayclose == False:
                    # terminal_ids.append(terminal.terminal_no)
            return Response({"detail": f"Terminal : {terminal_to_close_their_day[0]} has bill and need to close their days "}, status=status.HTTP_400_BAD_REQUEST)
                    
            # return Response({"detail": f"There exists some terminal whose day is not closed"}, status=status.HTTP_400_BAD_REQUEST)


        
        
        return Response({"detail": "Endday has been done successfully"}, status=status.HTTP_200_OK)


# from rest_framework.permissions import AllowAny
from organization.master_end_day import get_mobile_payments, get_payment_modes_summary, get_cash_total, get_credit_total, get_mobilepayment_total, get_complimentary_total, get_creditcard_total
class BranchTotalEndDay(APIView):

    def get(self, request, *args, **kwargs):

        from organization.utils import convert_to_dict, get_mobilepayments
        import pytz
        ny_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime_ny = timezone.now().astimezone(ny_timezone)

        formatted_date = current_datetime_ny.strftime("%Y-%m-%d")
        transaction_date = current_datetime_ny.date()
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("name")
            role = token_data.get("role")
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")

            # Print the branch
            print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        branch = Branch.objects.get(id=branch, is_deleted=False, status=True)
        from datetime import date, datetime
        today = date.today()
        enddays = EndDayDailyReport.objects.filter(branch=branch, created_date=today)
        print(enddays)
        enddays_terminal = []

        combine_data = {}
        total_sale_holder = 0.0
        net_sales_holder = 0.0
        discount_holder = 0.0
        tax_holder = 0.0

        total_dineintotalsale_holder = 0.0
        total_deliverytotalsale_holder =  0.0
        total_takeawaytotalsale_holder = 0.0
        total_dineinnettotal_holder = 0.0
        total_deliverynettotal_holder = 0.0
        total_takeawaynettotal_holder =  0.0
        total_dineinvattotal_holder = 0.0
        total_deliveryvattotal_holder =  0.0
        total_takeawayvattotal_holder = 0.0
        total_foodsale_holder = 0.0
        total_beveragesale_holder = 0.0
        total_otherssale_holder = 0.0
        total_tax_holder = 0.0  
        total_cash_holder = 0.0
        total_credit_holder = 0.0
        total_credit_card_holder = 0.0
        total_mobile_payment_holder = 0.0
        total_complimentary_holder = 0.0
        total_no_of_guest_holder = 0.0
        all_credit_bills = []
        all_discount_bills = []
        all_void_items = []
        dinnersales_holder = 0.0
        lunchsales_holder = 0.0
        # all_complementary_bills = []
        if enddays:

            for endday in enddays:
        
                # sender = env('EMAIL_HOST_USER')
                mail_list = True
                # recipients = MailRecipient.objects.filter(status=True)
                # for r in recipients:
                    # mail_list.append(r.email)
                    # MailSendRecord.objects.create(mail_recipient=r)
                if mail_list:
        
                    dt_now = datetime.now()
                    date_now = dt_now.date()
                    time_now = dt_now.time().strftime('%I:%M %p')
                    from organization.models import Organization
                    org = Organization.objects.first().org_name
                    
                    mobilepaymenttype_queryset, total_per_type = get_mobilepayments(endday.branch, endday.terminal)
                    mobilepaymenttype_dict = convert_to_dict(total_per_type) if mobilepaymenttype_queryset else None

                    
                    from bill.models import Bill
                    # bills = Bill.objects.filter(is_end_day=False, branch=endday.branch, terminal=endday.terminal)
                    bills = Bill.objects.filter(transaction_date=transaction_date, branch=endday.branch, terminal=endday.terminal)
                    total_transactions = bills.count()
                    total_grand_total_by_category = {}
        
                    for bill in bills:
                        for bill_item in bill.bill_items.all():
                            product_category = bill_item.product.type.title
        
                            total_grand_total_by_category[product_category] = (
                                total_grand_total_by_category.get(product_category, 0) + bill_item.amount 
                            )
        
                    print(total_grand_total_by_category)
        
                    # changes
        
                    cashdrops = CashDrop.objects.filter(branch_id=endday.branch, datetime__startswith=formatted_date)
                    print(f"CashDrops: {cashdrops}")  
                        # Calculate the total expense and total cashdrop
                    total_expense = cashdrops.aggregate(Sum('expense'))['expense__sum'] or 0.0
                    total_cashdrop = cashdrops.aggregate(Sum('cashdrop_amount'))['cashdrop_amount__sum'] or 0.0
                        
                    latest_balance=0
                    total_expense_cashdrop = 0
                    total_expense_cashdrop = total_expense + total_cashdrop
                    latest_cash_drop = cashdrops.last()
                    if latest_cash_drop is not None:
                            # Calculate the latest_balance
                        latest_balance = latest_cash_drop.opening_balance - latest_cash_drop.cashdrop_amount
                            # opening_balance = latest_cash_drop.opening_balance
                            # cashdrop = latest_cash_drop.cashdrop_amount
                        if latest_cash_drop.expense is not None:
                            latest_balance -= latest_cash_drop.expense
                                # expense = latest_cash_drop.expense
                        if latest_cash_drop.addCash is not None:
                            latest_balance += latest_cash_drop.addCash
                        else:
                            expense = 0.0
                        
                    opening_balance = latest_balance + total_expense_cashdrop
                    cash_to_be_added= float(endday.cash)
                    cash_total= latest_balance + cash_to_be_added
                    start_bill_number = int(endday.start_bill.split('-')[-1])
                    end_bill_number = int(endday.end_bill.split('-')[-1])
                    print(start_bill_number)
                    print(end_bill_number)
                        # bills = Bill.objects.filter(payment_mode="CREDIT")
                    from bill.models import Bill
                        # bills = Bill.objects.filter(payment_mode="CREDIT", invoice_number__gte=f'{instance.branch.branch_code}-{instance.terminal}-{start_bill_number}',
                        #     invoice_number__lte=f'{instance.branch.branch_code}-{instance.terminal}-{end_bill_number}', branch=instance.branch).values('invoice_number', 'customer_name', 'grand_total')
                    bills = Bill.objects.filter(
                        payment_mode="CREDIT",
                        invoice_number__range=[
                            f'{endday.branch.branch_code}-{endday.terminal}-{start_bill_number}',
                            f'{endday.branch.branch_code}-{endday.terminal}-{end_bill_number}'
                        ],
                        branch=endday.branch,
                        fiscal_year = get_current_fiscal_year()
                    ).values('invoice_number', 'customer_name', 'grand_total')
                    print("before sorting", bills)

                    credit_bills = bills
                    sorted_bills = sorted(bills, key=itemgetter('customer_name'))
                        
                    print("after sorting", sorted_bills)
                        # Group bills by customer_name
                    grouped_bills = {}
                    for key, group in groupby(sorted_bills, key=itemgetter('customer_name')):
                            # Convert the group iterator to a list of dictionaries
                        bills_data = list(group)
                        
                            # Calculate the total amount for each customer's bills
                        total_amount = sum(bill_data['grand_total'] for bill_data in bills_data)
                        
                            # Store the grouped data in a dictionary
                        grouped_bills[key] = {
                            'bills_data': bills_data,
                            'total_amount': total_amount
                        }
        
        #until here
                    from django.db.models import F
                    discount_bills = Bill.objects.filter(
                        discount_amount__gt=0,
                        invoice_number__range=[
                            f'{endday.branch.branch_code}-{endday.terminal}-{start_bill_number}',
                            f'{endday.branch.branch_code}-{endday.terminal}-{end_bill_number}'
                        ],
                        branch=endday.branch,
                        fiscal_year=get_current_fiscal_year()
                    ).annotate(
                    discount_name=F('discountId__discount_name'),# Rename 'discountId__discount_name' as 'discount_name'
                    discount_type=F('discountId__discount_type') #Rename 'discountId__discount_type ' as discount_type
                    ).values('invoice_number', 'customer_name', 'grand_total','payment_mode', 'discount_amount', 'discount_name', 'discount_type')

                    for_voiditem_bills = Bill.objects.filter(
                                            invoice_number__range=[
                                                f'{endday.branch.branch_code}-{endday.terminal}-{start_bill_number}',
                                                f'{endday.branch.branch_code}-{endday.terminal}-{end_bill_number}'
                                            ],
                                            branch=endday.branch
                                        ).values('invoice_number', 'customer_name', 'grand_total', 'discount_amount')
                    
                    from organization.master_end_day import get_void_items,get_lunch_sale, get_dinner_sale, get_complementary_bills

                    endday_terminal_bills = Bill.objects.filter(
                                            invoice_number__range=[
                                                f'{endday.branch.branch_code}-{endday.terminal}-{start_bill_number}',
                                                f'{endday.branch.branch_code}-{endday.terminal}-{end_bill_number}'
                                            ],
                                            branch=endday.branch
                                        )

                    void_items = get_void_items(for_voiditem_bills)
                    # dinnersales = get_dinner
                    lunchsales = get_lunch_sale(endday_terminal_bills)
                    dinnersales = get_dinner_sale(endday_terminal_bills)
                    print("lunch", lunchsales)
                    print(dinnersales)
                    void_items_list = []
                    for voiditem in void_items:
                        item = {'employee': 'test',
                                'item':voiditem.product.title,
                                'order':voiditem.order.id,
                                'quantity':voiditem.quantity,
                                'reason':voiditem.reason,
                                'value': round(float(voiditem.product.price) * float(voiditem.quantity), 2)}

                        void_items_list.append(item)
                    complementary_bills = get_complementary_bills(branch)
                    print("before sorting", bills)

                    credit_bills = bills
                    report_data = {
                        # 'dine_totalsale': endday.dine_grandtotal,
                        # 'delivery_totalsale': endday.delivery_grandtotal,
                        # 'takeaway_totalsale': endday.takeaway_grandtotal,
                        # 'dine_netsale': endday.dine_nettotal, 
                        # 'delivery_netsale': endday.delivery_nettotal, 
                        # 'takeaway_netsale': endday.takeaway_nettotal, 
                        # 'dine_vat': endday.dine_vattotal,
                        # 'delivery_vat': endday.delivery_vattotal,
                        # 'takeaway_vat': endday.takeaway_vattotal,   
                        # 'total_sale': endday.total_sale,
                        # 'date_time':endday.date_time,
                        # 'employee_name': endday.employee_name,
                        # 'net_sales': endday.net_sales,
                        # 'tax': endday.vat,  
                        # 'total_discounts': endday.total_discounts,
                        # 'cash': endday.cash,
                        # 'credit': endday.credit,
                        # 'credit_card': endday.credit_card,
                        # 'mobile_payment': endday.mobile_payment,
                        # 'complimentary': endday.complimentary,
                        'start_bill': endday.start_bill,
                        'end_bill': endday.end_bill,
                        'branch': endday.branch.name,
                        'terminal': endday.terminal,
                        # 'total_transactions': total_transactions,
                        # 'total_grand_total_by_category':total_grand_total_by_category,
                        # 'grouped_bills': grouped_bills,
                        # 'food_sale': endday.food_sale,
                        # 'beverage_sale': endday.beverage_sale,
                        # 'others_sale': endday.others_sale,
                        # 'cash_total': cash_total,
                        # 'latest_balance': latest_balance,
                        # 'opening_balance': opening_balance,
                        # 'total_expense': total_expense,
                        # 'no_of_guest': endday.no_of_guest,
                        # 'total_cashdrop': total_cashdrop,  # Include the total expense and cashdrop in report_data
                        # 'mobilepaymenttype_dict': mobilepaymenttype_dict if mobilepaymenttype_dict else None,
                        # 'credit_bills':credit_bills,
                        # 'discount_bills':discount_bills,
                        # 'void_items': void_items_list,
                        # 'lunchsales':lunchsales,
                        # 'dinnersales':dinnersales,
                        # 'complementary_bills':complementary_bills,

                    }
        
        
        
                    enddays_terminal.append(report_data)
                    total_sale_holder += endday.total_sale
                    net_sales_holder += endday.net_sales
                    discount_holder += endday.total_discounts
                    tax_holder += endday.vat
                    total_dineintotalsale_holder += endday.dine_grandtotal
                    total_deliverytotalsale_holder += endday.delivery_grandtotal
                    total_takeawaytotalsale_holder += endday.takeaway_grandtotal
                    total_dineinnettotal_holder += endday.dine_nettotal
                    total_deliverynettotal_holder += endday.delivery_nettotal
                    total_takeawaynettotal_holder += endday.takeaway_nettotal
                    total_dineinvattotal_holder += endday.dine_vattotal
                    total_deliveryvattotal_holder += endday.delivery_vattotal
                    total_takeawayvattotal_holder += endday.takeaway_vattotal
                    total_foodsale_holder += endday.food_sale
                    total_beveragesale_holder += endday.beverage_sale
                    total_otherssale_holder += endday.others_sale
                    total_cash_holder += endday.cash
                    total_credit_holder += endday.credit
                    total_credit_card_holder += endday.credit_card
                    total_mobile_payment_holder += endday.mobile_payment
                    total_complimentary_holder += endday.complimentary
                    total_no_of_guest_holder += endday.no_of_guest
                    for credit_bill in credit_bills:
                        all_credit_bills.append(credit_bill)
                    for discount_bill in discount_bills:
                        all_discount_bills.append(discount_bill)
                    # for complementary_bill in complementary_bills:
                    #     all_complementary_bills.append(complementary_bill)

                    for it in void_items_list:
                        all_void_items.append(it)
                    dinnersales_holder += dinnersales
                    lunchsales_holder += lunchsales



                # setting the mobiletypequeryset as already sent in mail so that it wont go again in another endday
                if mobilepaymenttype_queryset is not None:
                    for payment in mobilepaymenttype_queryset:
                        payment.sent_in_mail = True
                        payment.save()
                    # print()

        
                    # Inside the create_profile function
            
                    # Thread(target=send_combined_mail_to_receipients, args=(combine_data, enddays_terminal, mail_list, sender)).start()
                print(f"mail_list {mail_list}")
            payment_modes_summary =  get_payment_modes_summary(branch)
            print("payment_modes_summary", payment_modes_summary)
            combine_data = {
                        'org_name':org,
                        'branch': branch.name,
                        'date_now': date_now,
                        'time_now': time_now,
                        "total_sale": total_sale_holder,
                        "net_sales": net_sales_holder,
                        "tax": tax_holder,
                        "total_discounts": discount_holder,
                        "dinein_total": total_dineintotalsale_holder,
                        "delivery_total":total_deliverytotalsale_holder,
                        "takeaway_total":total_takeawaytotalsale_holder,
                        "dinein_net": total_dineinnettotal_holder,
                        "delivery_net":total_deliverynettotal_holder,
                        "takeaway_net":total_takeawaynettotal_holder,
                        "dinein_vat": total_dineinvattotal_holder,
                        "delivery_vat":total_deliveryvattotal_holder,
                        "takeaway_vat":total_takeawayvattotal_holder,
                        "total_foodsale": total_foodsale_holder,
                        "total_beveragesale": total_beveragesale_holder,
                        "total_otherssale": total_otherssale_holder,
                        "total_tax" : total_tax_holder,  
                        "total_cash":get_cash_total(payment_modes_summary),
                        "total_credit":get_credit_total(payment_modes_summary),
                        "total_creditcard":get_creditcard_total(payment_modes_summary),
                        "total_mobilepayment":get_mobilepayment_total(payment_modes_summary),
                        "total_complimentary":get_complimentary_total(payment_modes_summary),
                        "total_no_of_guest":total_no_of_guest_holder,
                        "credit_bills": all_credit_bills,
                        "discount_bills": all_discount_bills,
                        "all_void_items":all_void_items,
                        'total_lunchsales': lunchsales_holder,
                        'total_dinnersales': dinnersales_holder,
                        'complementary_bills':complementary_bills,
                        'terminals': enddays_terminal,
                        'mobile_payments': get_mobile_payments(branch)

                    }
            print(f"enddays_terminal {enddays_terminal}")
            return Response(
                {"combined_data": combine_data}, 200)
        else:
            return Response("Endday has not been created", 400)
    
class LastTerminalCheck(APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("name")
            role = token_data.get("role")
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")

            # Print the branch
            print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        branch = Branch.objects.get(id=branch, is_deleted=False, status=True)

        terminal_no = kwargs.get('terminal_no')
        from datetime import date
        today = date.today()
        print(today)
        terminal = Terminal.objects.filter(branch=branch, terminal_no=int(terminal_no), status=True, is_deleted=False).first()

        all_terminals_for_that_branch = Terminal.objects.filter(Q(branch=branch), ~Q(terminal_no=int(terminal_no)), status=True, is_deleted=False)
        print(all_terminals_for_that_branch)
        is_last_terminal = True
        for terminal in all_terminals_for_that_branch:

            if not EndDayDailyReport.objects.filter(
                created_date=today, 
                terminal=str(terminal.terminal_no), 
                branch=branch).exists():
                if Bill.objects.filter(is_end_day=False, status=True, terminal=terminal.terminal_no, branch=branch).exists():
                    is_last_terminal = False
                    break
        
        return Response({'is_last_terminal': is_last_terminal}, 200)
    
from organization.master_end_day import fetch_details_for_one_endday
class MailCheck(APIView):

    def get(self, request):
        endday = EndDayDailyReport.objects.last()

        fetch_details_for_one_endday(endday)

        return Response("Mail Sent", 200)
    
from django.utils.dateparse import parse_date
from organization.todays_sales_data import get_payment_modes_summary_todays_sales, get_complementary_bills_todays_sales,get_mobile_payments_todays_sales
class BranchTodaysSalesDateWise(APIView):

    def get(self, request, *args, **kwargs):

        from_date_str = request.GET.get('fromDate')
        to_date_str = request.GET.get('toDate')
        branch_id_get = request.GET.get('branch')
        if not (from_date_str and to_date_str):
            return Response("Please provide date", 400)

        # Parse dates from strings
        from_date = parse_date(from_date_str)
        to_date = parse_date(to_date_str)

        from organization.utils import convert_to_dict, get_mobilepayments
        import pytz
        ny_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime_ny = timezone.now().astimezone(ny_timezone)

        formatted_date = current_datetime_ny.strftime("%Y-%m-%d")
        transaction_date = current_datetime_ny.date()
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("name")
            role = token_data.get("role")
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            # branch = token_data.get("branch")

            # # Print the branch
            # print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        try:
            branch = Branch.objects.get(id=int(branch_id_get), is_deleted=False, status=True)
        except Exception as e:
            return Response("No branch found", 400)
        from datetime import date, datetime
        today = date.today()
        # enddays = EndDayDailyReport.objects.filter(branch=branch, created_date__range=today)
        # print(enddays)
        enddays_terminal = []

        combine_data = {}
        total_sale_holder = 0.0
        net_sales_holder = 0.0
        discount_holder = 0.0
        tax_holder = 0.0

        total_foodsale_holder = 0.0
        total_beveragesale_holder = 0.0
        total_otherssale_holder = 0.0
        total_no_of_guest_holder = 0.0
        # all_credit_bills = []
        # all_discount_bills = []
        dinnersales_holder = 0.0
        lunchsales_holder = 0.0
        


        if from_date and to_date:
            # If from_date and to_date are equal, get bills for that single day
            if from_date == to_date:
                queryset1 = Bill.objects.filter(branch=branch, transaction_date=from_date)
            else:
                # Otherwise, get bills where transaction_date is between from_date and to_date (inclusive)
                queryset1 = Bill.objects.filter(branch=branch, transaction_date__range=(from_date, to_date))
        else:
            return Response("Invalid or missing date range", 400)

        dt_now = datetime.now()
        date_now = dt_now.date()
        time_now = dt_now.time().strftime('%I:%M %p')
        from organization.models import Organization
        org = Organization.objects.first().org_name
                    
        # from bill.models import Bill
        # bills = Bill.objects.filter(transaction_date=transaction_date, branch=branch, terminal=endday.terminal)
        # total_transactions = bills.count()
        # total_grand_total_by_category = {}
        

        credit_bills = queryset1.filter(
        payment_mode="CREDIT",
        ).values('invoice_number', 'customer_name', 'grand_total')

        # credit_bills = bills
        # sorted_bills = sorted(bills, key=itemgetter('customer_name'))
        
        #until here
        from django.db.models import F
        discount_bills = queryset1.filter(
                discount_amount__gt=0,
        ).annotate(
        discount_name=F('discountId__discount_name'),# Rename 'discountId__discount_name' as 'discount_name'
        discount_type=F('discountId__discount_type') #Rename 'discountId__discount_type ' as discount_type
        ).values('invoice_number', 'customer_name', 'grand_total','payment_mode', 'discount_amount', 'discount_name', 'discount_type')

        # for_voiditem_bills = Bill.objects.filter(
        #                                     branch=branch
        #                                 ).values('invoice_number', 'customer_name', 'grand_total', 'discount_amount')
                    
        from organization.master_end_day import get_void_items,get_lunch_sale, get_dinner_sale

        void_items = get_void_items(queryset1)
                    # dinnersales = get_dinner
        lunchsales = get_lunch_sale(queryset1)
        dinnersales = get_dinner_sale(queryset1)
        print("lunch", lunchsales)
        print(dinnersales)
        void_items_list = []
        for voiditem in void_items:
            item = {'employee': 'test',
                                'item':voiditem.product.title,
                                'order':voiditem.order.id,
                                'quantity':voiditem.quantity,
                                'reason':voiditem.reason,
                                'value': round(float(voiditem.product.price) * float(voiditem.quantity), 2)}

            void_items_list.append(item)
        complementary_bills = get_complementary_bills_todays_sales(queryset1)
        # print("before sorting", bills)

        # credit_bills = bills
        

        payment_modes_summary =  get_payment_modes_summary_todays_sales(queryset1)
        print("payment_modes_summary", payment_modes_summary)

        from decimal import Decimal
        from product.models import Product
        sub_total_sum = Decimal(0)
        discount_holder = Decimal(0)
        taxable_amount_sum = Decimal(0)
        tax_holder = Decimal(0)
        grand_total_sum = Decimal(0)
        service_charge_sum = Decimal(0)
        print(queryset1)
        for bill in queryset1:
            if bill.payment_mode != "COMPLIMENTARY":
                sub_total_sum += bill.sub_total
                discount_holder += bill.discount_amount
                taxable_amount_sum += bill.taxable_amount
                tax_holder += bill.tax_amount
                grand_total_sum += bill.grand_total
                service_charge_sum += bill.service_charge
        net_sales_holder = sub_total_sum - discount_holder

                
        dine_in_bills_sub_total = queryset1.filter(order__order_type="Dine In").aggregate(sub_total_sum=Sum('sub_total'))['sub_total_sum']
        takeaway_bills_sub_total = queryset1.filter(order__order_type="Takeaway").aggregate(sub_total_sum=Sum('sub_total'))['sub_total_sum']
        delivery_bills_sub_total = queryset1.filter(order__order_type="Delivery").aggregate(sub_total_sum=Sum('sub_total'))['sub_total_sum']
        dine_in_bills_vat_total = queryset1.filter(order__order_type="Dine In").aggregate(tax_amount_sum=Sum('tax_amount'))['tax_amount_sum']
        takeaway_bills_vat_total = queryset1.filter(order__order_type="Takeaway").aggregate(tax_amount_sum=Sum('tax_amount'))['tax_amount_sum']
        delivery_bills_vat_total = queryset1.filter(order__order_type="Delivery").aggregate(tax_amount_sum=Sum('tax_amount'))['tax_amount_sum']
        dine_in_bills_discount_total = queryset1.filter(order__order_type="Dine In").aggregate(discount_amount_sum=Sum('discount_amount'))['discount_amount_sum']
        takeaway_bills_discount_total = queryset1.filter(order__order_type="Takeaway").aggregate(discount_amount_sum=Sum('discount_amount'))['discount_amount_sum']
        delivery_bills_discount_total = queryset1.filter(order__order_type="Delivery").aggregate(discount_amount_sum=Sum('discount_amount'))['discount_amount_sum']

        dine_in_bills_netsale = (dine_in_bills_sub_total if dine_in_bills_sub_total else Decimal(0.0)) - (dine_in_bills_discount_total if dine_in_bills_discount_total else Decimal(0.0))
        takeaway_bills_netsale = (takeaway_bills_sub_total if takeaway_bills_sub_total else Decimal(0.0)) - (takeaway_bills_discount_total if takeaway_bills_discount_total else Decimal(0.0))
        delivery_bills_netsale = (delivery_bills_sub_total if delivery_bills_sub_total else Decimal(0.0)) - (delivery_bills_discount_total if delivery_bills_discount_total else Decimal(0.0))


        dine_in_bills_totalsale = Decimal(dine_in_bills_netsale) + (dine_in_bills_vat_total if dine_in_bills_vat_total else Decimal(0.0))
        delivery_bills_totalsale = Decimal(delivery_bills_netsale) + (delivery_bills_vat_total if delivery_bills_vat_total else Decimal(0.0))
        takeaway_bills_totalsale = Decimal(takeaway_bills_netsale) + (takeaway_bills_vat_total if takeaway_bills_vat_total else Decimal(0.0))




        total_foodsale_holder = queryset1.filter(
            bill_items__product_title__in=Product.objects.filter(type__title="FOOD").values_list('title', flat=True)
        ) .aggregate(food_total=Sum('bill_items__amount'))['food_total'] or Decimal(0)
                # print(food_total)

                # print(food_total)

                # Get the total amount of beverage products
        total_beveragesale_holder = queryset1.filter(
            bill_items__product_title__in=Product.objects.filter(type__title="BEVERAGE").values_list('title', flat=True)
        ).aggregate(beverage_total=Sum('bill_items__amount'))['beverage_total'] or Decimal(0)

                # Get the total amount of other products
        total_otherssale_holder = queryset1.filter(
            bill_items__product_title__in=Product.objects.filter(type__title="OTHERS").values_list('title', flat=True)
        ).aggregate(others_total=Sum('bill_items__amount'))['others_total'] or Decimal(0)



        for bill in queryset1:
            order = bill.order
            if order is not None:
                total_no_of_guest_holder += order.no_of_guest

        terminals = Terminal.objects.filter(branch=branch, status=True, is_deleted=False)

        for terminal in terminals:
            terminal_bills = queryset1.filter(terminal=terminal.terminal_no).order_by('id')
            if terminal_bills:
                terminal_data = {
                    'terminal':terminal.terminal_no,
                    'start_bill': terminal_bills.first().invoice_number if terminal_bills else None,
                    'end_bill': terminal_bills.last().invoice_number if terminal_bills else None,
                    'branch':branch.name
                }
                enddays_terminal.append(terminal_data)

        combine_data = {
                        'org_name':org,
                        'branch': branch.name,
                        'date_now': date_now,
                        'time_now': time_now,
                        "total_sale": grand_total_sum,
                        "net_sales": net_sales_holder,
                        "tax": tax_holder,
                        "total_discounts": discount_holder,
                        "dinein_total": dine_in_bills_totalsale,
                        "delivery_total":delivery_bills_totalsale,
                        "takeaway_total":takeaway_bills_totalsale,
                        "dinein_net": dine_in_bills_netsale,
                        "delivery_net":delivery_bills_netsale,
                        "takeaway_net":takeaway_bills_netsale,
                        "dinein_vat": dine_in_bills_vat_total,
                        "delivery_vat":delivery_bills_vat_total,
                        "takeaway_vat":takeaway_bills_vat_total,
                        "total_foodsale": total_foodsale_holder,
                        "total_beveragesale": total_beveragesale_holder,
                        "total_otherssale": total_otherssale_holder,
                        # "total_tax" : total_tax_holder,  
                        "total_cash":get_cash_total(payment_modes_summary),
                        "total_credit":get_credit_total(payment_modes_summary),
                        "total_creditcard":get_creditcard_total(payment_modes_summary),
                        "total_mobilepayment":get_mobilepayment_total(payment_modes_summary),
                        "total_complimentary":get_complimentary_total(payment_modes_summary),
                        "total_no_of_guest":total_no_of_guest_holder,
                        "credit_bills": credit_bills,
                        "discount_bills": discount_bills,
                        "all_void_items":void_items_list,
                        'total_lunchsales': lunchsales,
                        'total_dinnersales': dinnersales,
                        'complementary_bills':complementary_bills,
                        'terminals': enddays_terminal,
                        'mobile_payments': get_mobile_payments_todays_sales(queryset1)

                    }
        print(f"enddays_terminal {enddays_terminal}")
        return Response(
                {"combined_data": combine_data}, 200)