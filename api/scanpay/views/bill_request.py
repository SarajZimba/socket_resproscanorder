# from api.scanpay.serializers.bill_request import BillRequestSerializer 
# from rest_framework.response import Response

# from rest_framework.views import APIView
# from order.models import BillRequest

# class BillRequestAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet')
#         try:
#             billrequest_data = request.data
#             billrequest_data['outlet'] = outlet
#             serializer = BillRequestSerializer(data=billrequest_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response("Bill request Done successfully", 200)
#             else:
#                 # Print or log the validation errors
#                 print(serializer.errors)  # This will print errors to the console
#                 return Response({"detail":"Bill request for this order has been made already"}, 400)
#         except Exception as e:
#             return Response("Error occured while creating bill request", 400)
        
# import pytz
# from django.utils import timezone

# class BillRequestConfirmAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         billrequest_id = kwargs.get('billrequest_id')
#         desired_timezone = pytz.timezone('Asia/Kathmandu')
#         current_datetime = timezone.now().astimezone(desired_timezone)

#         # Format the datetime as a string
#         current_datetime_str = current_datetime.strftime('%Y-%m-%d %I:%M %p')
#         try:
#             billrequest = BillRequest.objects.get(pk=billrequest_id)
#             billrequest.completed_time = current_datetime_str
#             billrequest.is_completed = True
#             billrequest.save()

#             return Response("Bill request completed Successfully, 200")
#         except Exception as e:
#             return Response("No Billrequest found with such id", 400)
        
# class BillRequestListAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         outlet = kwargs.get('outlet')

#         billrequests = BillRequest.objects.filter(is_deleted = False, outlet=outlet, is_completed=False)

#         serailizer = BillRequestSerializer(billrequests, many=True)

#         return Response(serailizer.data, 200)
        

# from order.models import ScanPayOrder
# class BillRequestwithDiscountAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         order = kwargs.get('order')
#         order_obj = ScanPayOrder.objects.get(pk=order)
#         order_obj.billreqwithdiscount = True
#         order_obj.save()

#         return Response("billreqwithdiscount flag set true", 200)

from api.scanpay.serializers.bill_request import BillRequestSerializer 
from rest_framework.response import Response

from rest_framework.views import APIView
from order.models import BillRequest

from rest_framework.permissions import AllowAny

class BillRequestAPIView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet')
        try:
            billrequest_data = request.data
            billrequest_data['outlet'] = outlet
            serializer = BillRequestSerializer(data=billrequest_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Bill request Done successfully", 200)
            else:
                # Print or log the validation errors
                print(serializer.errors)  # This will print errors to the console
                return Response({"detail":"Bill request for this order has been made already"}, 400)
        except Exception as e:
            return Response("Error occured while creating bill request", 400)
        
import pytz
from django.utils import timezone

class BillRequestConfirmAPIView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        billrequest_id = kwargs.get('billrequest_id')
        desired_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime = timezone.now().astimezone(desired_timezone)

        # Format the datetime as a string
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %I:%M %p')
        try:
            billrequest = BillRequest.objects.get(pk=billrequest_id)
            billrequest.completed_time = current_datetime_str
            billrequest.is_completed = True
            billrequest.save()

            return Response("Bill request completed Successfully, 200")
        except Exception as e:
            return Response("No Billrequest found with such id", 400)
        
class BillRequestListAPIView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet')

        billrequests = BillRequest.objects.filter(is_deleted = False, outlet=outlet, is_completed=False)

        serailizer = BillRequestSerializer(billrequests, many=True)

        return Response(serailizer.data, 200)
        

from order.models import ScanPayOrder
class BillRequestwithDiscountAPIView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        order = kwargs.get('order')
        order_obj = ScanPayOrder.objects.get(pk=order)
        order_obj.billreqwithdiscount = True
        order_obj.save()

        return Response("billreqwithdiscount flag set true", 200)
