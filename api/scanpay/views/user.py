# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from user.models import UserLogin
# from api.scanpay.serializers.user import UserLoginSerializer

# class UserLoginCreateAPIView(APIView):
#     def post(self, request, format=None):
#         device_token = request.data['device_token']
#         previous_logins = UserLogin.objects.filter(device_token=device_token)
#         if previous_logins:
#             previous_logins.delete()
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserLogin
from api.scanpay.serializers.user import UserLoginSerializer
from rest_framework.permissions import AllowAny

class UserLoginCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        device_token = request.data['device_token']
        previous_logins = UserLogin.objects.filter(device_token=device_token)
        if previous_logins:
            previous_logins.delete()
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


