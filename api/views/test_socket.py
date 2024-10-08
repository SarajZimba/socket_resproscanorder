from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from discount.models import DiscountTable
from api.serializers.discount import DiscountSerilizer
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# api to get all the discounts
class TestSocket(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        channel_layer = get_channel_layer()
        # for instance in my_model_instances:
        #     self.stdout.write(self.style.SUCCESS(instance.__str__()))  # Print each instance
        print("hello")
        async_to_sync(
            channel_layer.group_send)("chat_group",{
                "type": "chat_message",
                "message": "Demo notification"
            }
        )        

        return Response('success', status=status.HTTP_200_OK)