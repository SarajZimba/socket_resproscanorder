# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from discounts.models import discountflag, tbl_discounts
# from api.scanpay.serializers.discount import TimedDiscountSerializer, DiscountSerializer

# class CreateTimedDiscountView(APIView):
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         discount = request.data[0]['discount']  
#         print(f'discount {discount}')
#         previous_entry = discountflag.objects.filter(discount__id = discount)
#         print(previous_entry)
#         if previous_entry:
#             previous_entry.delete()
#         serializer = TimedDiscountSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             instances = [discountflag(**item) for item in serializer.validated_data]
#             discountflag.objects.bulk_create(instances)
#             return Response({"status": "success"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




# class DiscountCreateView(APIView):

#     def post(self, request):
#         discounts_data = request.data
        
#         if not isinstance(discounts_data, list):
#             return Response({"error": "Expected a list of discount objects."}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = DiscountSerializer(data=discounts_data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# from datetime import datetime   
# from django.utils import timezone
# class DiscountList(APIView):
#     pass

#     def get(self, request, *args, **kwargs):

#         discounts = tbl_discounts.objects.filter(status=True, is_deleted=False)

#         discount_sent = []

#         for discount in discounts:
#             if discount.is_timed == True:
#                 timeddiscount = discountflag.objects.filter(discount=discount)
#                 current_day = datetime.now().strftime('%A')  # Get current day of the week
#                 current_time = datetime.now().time()  # Get current time  
#                 if timeddiscount:
#                     timed_discount_day = timeddiscount.filter(dayofweek=current_day).first()
#                     if timed_discount_day:

#                         if timed_discount_day.state == True:
#                             start_time = timed_discount_day.start_time
#                             end_time = timed_discount_day.end_time

#                             if  current_time >= start_time and current_time <= end_time:
#                                 discount_data = {
#                                     'start_time': start_time,
#                                     'end_time':end_time,
#                                     'name' : discount.name,
#                                     'type': discount.type,
#                                     'value': discount.value,
#                                     'is_timed': discount.is_timed,
#                                     'state': timed_discount_day.state
#                                 }
#                                 discount_sent.append(discount_data)
                      
#             else:
#                 discount_data = {
#                                     'start_time': None,
#                                     'end_time':None,
#                                     'name' : discount.name,
#                                     'type': discount.type,
#                                     'value': discount.value,
#                                     'is_timed': discount.is_timed,
#                                     'state': 'false'
#                         }                
#                 discount_sent.append(discount_data) 
#         return Response(discount_sent, 200)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from discounts.models import discountflag, tbl_discounts
from api.scanpay.serializers.discount import TimedDiscountSerializer, DiscountSerializer
from rest_framework.permissions import AllowAny

class CreateTimedDiscountView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        discount = request.data[0]['discount']  
        print(f'discount {discount}')
        previous_entry = discountflag.objects.filter(discount__id = discount)
        print(previous_entry)
        if previous_entry:
            previous_entry.delete()
        serializer = TimedDiscountSerializer(data=request.data, many=True)
        if serializer.is_valid():
            instances = [discountflag(**item) for item in serializer.validated_data]
            discountflag.objects.bulk_create(instances)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class DiscountCreateView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        discounts_data = request.data
        
        if not isinstance(discounts_data, list):
            return Response({"error": "Expected a list of discount objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DiscountSerializer(data=discounts_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# from menu.models import FlagMenu
# class DiscountStatus(APIView):
#     def get(self, request, *args, **kwargs):
#         discount_status = FlagMenu.objects.first().allow_discount

#         return Response({'allow_discount': discount_status}, 200)
        
from datetime import datetime   
from django.utils import timezone
class DiscountList(APIView):
    
    permission_classes = [AllowAny]
    pass

    def get(self, request, *args, **kwargs):

        discounts = tbl_discounts.objects.filter(status=True, is_deleted=False)

        discount_sent = []

        for discount in discounts:
            if discount.is_timed == True:
                timeddiscount = discountflag.objects.filter(discount=discount)
                current_day = datetime.now().strftime('%A')  # Get current day of the week
                current_time = datetime.now().time()  # Get current time  
                if timeddiscount:
                    timed_discount_day = timeddiscount.filter(dayofweek=current_day).first()
                    if timed_discount_day:

                        if timed_discount_day.state == True:
                            start_time = timed_discount_day.start_time
                            end_time = timed_discount_day.end_time

                            if  current_time >= start_time and current_time <= end_time:
                                discount_data = {
                                    'start_time': start_time,
                                    'end_time':end_time,
                                    'name' : discount.name,
                                    'type': discount.type,
                                    'value': discount.value,
                                    'is_timed': discount.is_timed,
                                    'state': timed_discount_day.state
                                }
                                discount_sent.append(discount_data)

                        # else:
                        #     discount_data = {
                        #             'start_time': None,
                        #             'end_time':None,
                        #             'name' : discount.name,
                        #             'type': discount.type,
                        #             'value': discount.value,
                        #             'is_timed': discount.is_timed,
                        #             'state': timed_discount_day.state
                        #         }
                        #     discount_sent.append(discount_data)                            
            else:
                discount_data = {
                                    'start_time': None,
                                    'end_time':None,
                                    'name' : discount.name,
                                    'type': discount.type,
                                    'value': discount.value,
                                    'is_timed': discount.is_timed,
                                    'state': 'false'
                        }                
                discount_sent.append(discount_data) 
        return Response(discount_sent, 200)
