from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import tblModifications
from rest_framework.permissions import AllowAny

from api.serializers.modifications import ModificatinsSerializer
class ModificationAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get('id')
        try:
            modifications = tblModifications.objects.filter(product__id=menu_id)
            serializer = ModificatinsSerializer(modifications, many=True)   
            return Response(serializer.data, status=200)
        except Exception as e:
            print(e)
            return Response("Something went wrong", status=400)