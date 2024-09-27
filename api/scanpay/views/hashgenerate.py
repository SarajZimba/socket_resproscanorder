# from rest_framework.views import APIView
# from api.scanpay.serializers.hashgenerate import HashValueSerializer
# from rest_framework.response import Response
# from order.models import HashValue

# class HashAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         posted_data = request.data
#         outlet = posted_data['outlet']
#         table = posted_data['table']
#         try:
#             serializer = HashValueSerializer(data=posted_data)

#             if serializer.is_valid():
#                 hashvalue_obj = HashValue.objects.filter(outlet=outlet, table=table)
#                 if hashvalue_obj:
#                     hashvalue_obj.delete()

#                 hashvalue_obj = serializer.save()

#                 hashvalue = hashvalue_obj.hash_value

#                 # return Response({"hashvalue": f"backend.silverlimenu.silverlinepos.com/{hashvalue}"}, 200)
#                 return Response({"hashvalue": hashvalue}, 200)

#             else:
#                 return Response(e, 400)
#         except Exception as e:
#             return Response(e, 400)        

# from menu.models import Organization
# class GiveTableOutletHashAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         hashvalue = kwargs.get('hashvalue')
#         org = Organization.objects.first()
#         try:
#             hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
#             dict = {
#                 "org_name": org.name,
#                 "org_address": org.address, 
#                 "org_logo": org.org_logo.url if org.org_logo else None, 
#                 "background_image": org.background_image.url if org.background_image else None,
#                 "outlet": hashvalue_obj.outlet, 
#                 "table_no": hashvalue_obj.table
#             }
#             return Response(dict, 200)
#         except Exception as e:
#             return Response(e, 400)
        
# class ClearHashValue(APIView):
#     def get(self, request, *args, **kwargs):
#         hashvalue = kwargs.get('hashvalue')
#         try:
#             hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
#             hashvalue_obj.delete()
#             return Response("Hash object deleted successfully", 200)
#         except Exception as e:
#             return Response(e, 400)


from rest_framework.views import APIView
from api.scanpay.serializers.hashgenerate import HashValueSerializer
from rest_framework.response import Response
from order.models import HashValue
from rest_framework.permissions import AllowAny

class HashAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        posted_data = request.data
        outlet = posted_data['outlet']
        table = posted_data['table']
        try:
            serializer = HashValueSerializer(data=posted_data)

            if serializer.is_valid():
                hashvalue_obj = HashValue.objects.filter(outlet=outlet, table=table)
                if hashvalue_obj:
                    hashvalue_obj.delete()

                hashvalue_obj = serializer.save()

                hashvalue = hashvalue_obj.hash_value

                return Response({"hashvalue": hashvalue}, 200)

            else:
                return Response(e, 400)
        except Exception as e:
            return Response(e, 400)        

from organization.models import Organization
class GiveTableOutletHashAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        hashvalue = kwargs.get('hashvalue')
        org = Organization.objects.first()
        try:
            hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
            dict = {
                "org_name": org.org_name,
                "org_address": org.company_address, 
                "org_logo": org.org_logo.url if org.org_logo else None, 
                "background_image": org.background_image.url if org.background_image else None,
                "outlet": hashvalue_obj.outlet, 
                "table_no": hashvalue_obj.table
            }
            return Response(dict, 200)
        except Exception as e:
            return Response(e, 400)
# from order.utils import get_terminal_obj

# from organization.models import Organization, Branch, Table
# class GiveTableOutletHashAPIView(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request, *args, **kwargs):
#         hashvalue = kwargs.get('hashvalue')
#         org = Organization.objects.first()
#         try:
#             hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
#             table_no = hashvalue_obj.table
#             outlet = hashvalue_obj.outlet

#             branch = Branch.objects.filter(branch_code=outlet, status=True, is_deleted=False).first()

#             terminal_obj = get_terminal_obj(branch, table_no)

#             table = Table.objects.filter(terminal=terminal_obj, table_number=table_no, is_deleted=False, status=True).first()

#             if table.is_occupied == True:
#                 return Response("This table is already occupied", 400)
#             else:
#                 dict = {
#                     "org_name": org.org_name,
#                     "org_address": org.company_address, 
#                     "org_logo": org.org_logo.url if org.org_logo else None, 
#                     "background_image": org.background_image.url if org.background_image else None,
#                     "outlet": hashvalue_obj.outlet, 
#                     "table_no": hashvalue_obj.table
#                 }
#                 return Response(dict, 200)
#         except Exception as e:
#             print(e)
#             return Response(e, 400)
        
class ClearHashValue(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        hashvalue = kwargs.get('hashvalue')
        try:
            hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
            hashvalue_obj.delete()
            return Response("Hash object deleted successfully", 200)
        except Exception as e:
            return Response(e, 400)
