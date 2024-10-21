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



class BranchTotalEndDay(APIView):
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
        from datetime import date
        today = date.today()

        enddays = EndDayDailyReport.objects.filter(branch=branch, created_date=today)

        # Aggregate the sums of all the required fields
        totals = enddays.aggregate(
            total_net_sales=Sum('net_sales'),
            total_vat=Sum('vat'),
            total_discounts=Sum('total_discounts'),
            total_cash=Sum('cash'),
            total_credit=Sum('credit'),
            total_credit_card=Sum('credit_card'),
            total_mobile_payment=Sum('mobile_payment'),
            total_complimentary=Sum('complimentary'),
            total_void_count=Sum('total_void_count'),
            total_food_sale=Sum('food_sale'),
            total_beverage_sale=Sum('beverage_sale'),
            total_others_sale=Sum('others_sale'),
            total_no_of_guest=Sum('no_of_guest'),
            total_dine_grandtotal=Sum('dine_grandtotal'),
            total_delivery_grandtotal=Sum('delivery_grandtotal'),
            total_takeaway_grandtotal=Sum('takeaway_grandtotal'),
            total_dine_nettotal=Sum('dine_nettotal'),
            total_delivery_nettotal=Sum('delivery_nettotal'),
            total_takeaway_nettotal=Sum('takeaway_nettotal'),
            total_dine_vattotal=Sum('dine_vattotal'),
            total_delivery_vattotal=Sum('delivery_vattotal'),
            total_takeaway_vattotal=Sum('takeaway_vattotal'),
        )

        # Return the calculated totals in the response
        return Response({
            "branch": branch.name,
            "totals": totals
        }, 200)
    
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