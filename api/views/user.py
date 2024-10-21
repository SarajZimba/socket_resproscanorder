from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from user.models import Customer
from ..serializers.user import CustomTokenPairSerializer, CustomerSerializer

from organization.models import Terminal, Branch


from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import Group


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer


class CustomerAPI(ModelViewSet):
    serializer_class = CustomerSerializer
    model = Customer
    queryset = Customer.objects.active()
    pagination_class = None

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user import AgentSerializer

class AgentViewSet(viewsets.ViewSet):
    serializer_class = AgentSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            usercode = serializer.validated_data['username']
            full_name = serializer.validated_data['full_name']

            user = User.objects.create(username=usercode, full_name=full_name, is_superuser=False, is_staff=True)

            user.set_password(usercode)
            user.save()

            group = Group.objects.get(name="agent")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
        
            return Response({"detail":"User with the username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import AgentKitchenBar
from rest_framework.permissions import AllowAny

class AgentKitchenBarLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        # Extract username and password from the request
        usercode = data.get('username')
        password = data.get('password')

        # Check if the user exists
        users = AgentKitchenBar.objects.filter(username=usercode)

        # Handle cases based on the number of users found
        if users.count() == 0:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        elif users.count() > 1:
            return Response({'error': 'More than one user with the same username exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Only one user found, get the user object
        user = users.first()

        # Check the password
        if user.check_password(password):  # This method verifies the hashed password
            # Optionally, return user details or a token
            return Response({'full_name': user.full_name, 'email': user.email, 'branch':user.branch.branch_code if user.branch else None}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
