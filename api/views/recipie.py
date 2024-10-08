from rest_framework.views import APIView
from product.models import ProductRecipie
from api.serializers.recipie import RecipieSerializer
from rest_framework.response import Response
from product.models import Product
from rest_framework.permissions import AllowAny

class RecipieAPIView(APIView):

    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        recipieitem_id = kwargs.get('id')
        product = Product.objects.get(id=int(recipieitem_id))
        try:
            recipieitemobj = ProductRecipie.objects.get(product=product)
        except Exception as e:
            return Response("No recipie item found of that item", 400)


        serializer = RecipieSerializer(recipieitemobj)

        return Response(serializer.data, 200)

