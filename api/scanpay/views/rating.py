# from rating.models import tblitemRatings, tblRatings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from api.scanpay.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
# from django.db import transaction
# from order.models import ScanPayOrder
# from django.db.models import Q

# from rating.models import tblitemRatings, tblRatings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from api.scanpay.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
# from django.db import transaction
# from order.models import ScanPayOrder
# from django.db.models import Q
# from rating.mail import create_profile_for_email
# from rating.utils import give_review_points


# class RatingCreateAPIView(APIView):

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         table_no = data['table_no']
#         order = ScanPayOrder.objects.filter(Q(table_no=table_no) & (Q(state='Pending') | Q(state='Cooked')|Q(state='Accepted'))).first()
#         if order:
#             data['order'] = order.id
#         else:
#             return Response({"detail":"No order created first"}, 400)

#         if tblRatings.objects.filter(order=order).exists():
#             return Response({"detail": "Review already exists for this order"}, 400)
#         tblitemRatings = data.pop('tblitemRatings', [])
#         customer_name = data.get('customer_name', None)
#         customer_phone = data.get('customer_phone', None)
#         tblRatingsserializer = tblRatingSerializer(data=data)
#         if tblRatingsserializer.is_valid():
#             tblRating = tblRatingsserializer.save()
#         else: 
#             return Response("tblRating data is not valid", 400)
        
#         for item in tblitemRatings:
#             item['tblrating'] = tblRating.id
#         tblitemRatingSerializer = tblitemRatingsSerializer(data=tblitemRatings, many=True)
#         if tblitemRatingSerializer.is_valid():
#             tblitemRatingSerializer.save()

#         else:
#             return Response("tblitemRatings data is not valid", 400)
#         try:
#             give_review_points(customer_name, customer_phone)
#         except Exception as e:
#             print(e)
#             raise 
#         try:
#             create_profile_for_email(tblRating)
#         except Exception as e:
#             print(e)
#         return Response(tblRatingsserializer.data, 201)

from rating.models import tblitemRatings, tblRatings
from rest_framework.views import APIView
from rest_framework.response import Response
from api.scanpay.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
from django.db import transaction
from order.models import ScanPayOrder
from django.db.models import Q

from rating.models import tblitemRatings, tblRatings
from rest_framework.views import APIView
from rest_framework.response import Response
from api.scanpay.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
from django.db import transaction
from order.models import ScanPayOrder
from django.db.models import Q
from rating.mail import create_profile_for_email
from rating.utils import give_review_points
from rest_framework.permissions import AllowAny

class RatingCreateAPIView(APIView):
    
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        table_no = data['table_no']
        order = ScanPayOrder.objects.filter(Q(table_no=table_no) & (Q(state='Pending') | Q(state='Cooked')|Q(state='Accepted'))).first()
        if order:
            data['order'] = order.id
        else:
            return Response({"detail":"No order created first"}, 400)

        if tblRatings.objects.filter(order=order).exists():
            return Response({"detail": "Review already exists for this order"}, 400)
        tblitemRatings = data.pop('tblitemRatings', [])
        customer_name = data.get('customer_name', None)
        customer_phone = data.get('customer_phone', None)
        tblRatingsserializer = tblRatingSerializer(data=data)
        if tblRatingsserializer.is_valid():
            tblRating = tblRatingsserializer.save()
        else: 
            return Response("tblRating data is not valid", 400)
        
        for item in tblitemRatings:
            item['tblrating'] = tblRating.id
        tblitemRatingSerializer = tblitemRatingsSerializer(data=tblitemRatings, many=True)
        if tblitemRatingSerializer.is_valid():
            tblitemRatingSerializer.save()

        else:
            return Response("tblitemRatings data is not valid", 400)
        try:
            give_review_points(customer_name, customer_phone)
        except Exception as e:
            print(e)
            raise 
        try:
            create_profile_for_email(tblRating)
        except Exception as e:
            print(e)
        return Response(tblRatingsserializer.data, 201)

            



