from rest_framework.views import APIView
from bill.models import BillItemVoid
from rest_framework.response import Response
from django.db.models import Sum
import jwt
class VoidBillAPIView(APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")
            agent = token_data.get("name")

            # Print the branch
            print("Branch:", branch)
            print("Agent:", agent)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")

        # billitemvoids = BillItemVoid.objects.filter(status=True, is_deleted=False, order__branch=branch).values('product__title').annotate(total_quantity=Sum('quantity'))
        billitemvoids = BillItemVoid.objects.filter(status=True, is_deleted=False, order__branch=branch)
        void_list = []
        for itemvoids in billitemvoids:
            void_dict = {
                "product__title":itemvoids.product.title,
                "quantity": itemvoids.quantity,
                "start_time": itemvoids.order.created_at.strftime("%Y-%m-%d %I:%M %p"),
                "table_no": itemvoids.order.table_no,
                "reason": itemvoids.reason,
                "employee": itemvoids.order.employee

            }
            void_list.append(void_dict)
        # print(billitemvoids)

        
        return Response(void_list, 200)

from bill.models import tblOrderTracker
from api.serializers.order import tblOrderTrackerSerializer
# class VoidOrderTrackerAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         voidordertrackers = tblOrderTracker.objects.filter(
#             state='Void')
        
#         serializer = tblOrderTrackerSerializer(voidordertrackers, many=True)

#         return Response(serializer.data, 200)

from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import DateTimeField
from django.utils import timezone
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import AllowAny

class VoidOrderTrackerAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)

        product_type = request.data.get('product_type', None)
        # If no dates are provided, filter by today's date
        if not start_date and not end_date:
            today = timezone.now().date()
            voidordertrackers = tblOrderTracker.objects.filter(
                state='Void',
                ordertime__startswith=today.strftime("%Y-%m-%d")
            )
        else:
            # Parse the dates
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            # Convert dates to strings in the format "YYYY-MM-DD"
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            if product_type:
                if product_type == "Kitchen":
                    # Filter void order trackers based on date range by matching the string
                    voidordertrackers = tblOrderTracker.objects.filter(
                        Q(state='Void'),
                        Q(ordertime__gte=f"{start_date_str} 00:00:00 PM"),  # Adjusting time for the string format
                        Q(ordertime__lte=f"{end_date_str} 11:59:59 PM"),     # Adjusting time for the string format
                        ~Q(kotID=None)
                    )
                if product_type == "Bar":
                    # Filter void order trackers based on date range by matching the string
                    voidordertrackers = tblOrderTracker.objects.filter(
                        Q(state='Void'),
                        Q(ordertime__gte=f"{start_date_str} 00:00:00 PM"),  # Adjusting time for the string format
                        Q(ordertime__lte=f"{end_date_str} 11:59:59 PM"),     # Adjusting time for the string format
                        ~Q(botID=None)
                    )

        serializer = tblOrderTrackerSerializer(voidordertrackers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
