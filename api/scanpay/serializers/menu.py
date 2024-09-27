from rest_framework.serializers import Serializer, ModelSerializer
from menu.models import Menu
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

from menu.models import MenuType

class MenuSerializerCreate(ModelSerializer):

    class Meta:
        model = Menu
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "image_bytes", 
            "thumbnail"
        ]


    def create(self, validated_data):
        # image_bytes = validated_data.pop('image_bytes', None)
        # item_name = validated_data.get('item_name', None)
        return Menu.objects.create(**validated_data)

        # if image_bytes:
        #     menu.image_bytes = image_bytes
        #     menu.thumbnail = self.decode_image(image_bytes, item_name)
        #     menu.save()

        # return menu
    
    # def decode_image(self, image_bytes, item_name):
    #     try:
    #         decoded_img = base64.b64decode(image_bytes)

    #         image_file = ContentFile(decoded_img, name=f'{item_name}.jpg')
    #         return image_file
    #     except Exception as e:
    #         raise(e)


    
class MenuSerializerList(ModelSerializer):
    image_url = serializers.SerializerMethodField()
    imageList = serializers.SerializerMethodField()

    type = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_image_url(self, obj):
        return str("api/" + obj.item_name)
    
    def get_imageList(self, obj):
        media_files = MediaFile.objects.filter(product=obj)
        return MediaFileSerializer(media_files, many=True).data
    
    def get_type(self, obj):
        return obj.type.title()



# class MenuTypeSerializerList(ModelSerializer):
#         products = MenuSerializerList(source='menu_set', many=True, read_only=True) 
#         class Meta:       
#             model = MenuType
#             exclude = [
#                 "created_at",
#                 "updated_at",
#                 "status",
#                 "is_deleted",
#                 "sorting_order",
#                 "is_featured"
#             ]

# class MenuTypeSerializerListOutletWise(serializers.ModelSerializer):
#     products = MenuSerializerList(many=True, read_only=True) 

#     class Meta:
#         model = MenuType
#         exclude = [
#             "created_at",
#             "updated_at",
#             "status",
#             "is_deleted",
#             "sorting_order",
#             "is_featured"
#         ]

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
        
#         # Serialize the menus related to this MenuType
#         menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
#         serialized_menus = MenuSerializerList(menus, many=True, context=self.context).data
        
#         representation['products'] = serialized_menus
        
#         return representation

from menu.models import tbl_timedpromomenu
from datetime import datetime 
class MenuTypeSerializerList(ModelSerializer):
        products = MenuSerializerList(many=True, read_only=True) 
        start_time = serializers.SerializerMethodField()
        end_time = serializers.SerializerMethodField()
        class Meta:       
            model = MenuType
            exclude = [
                "created_at",
                "updated_at",
                "status",
                "is_deleted",
                "sorting_order",
                "is_featured"
            ]

        def get_start_time(self, obj):
            if obj.is_timed == True:
                timed_menu = tbl_timedpromomenu.objects.filter(menutype=obj)
                current_day = datetime.now().strftime('%A')  # Get current day of the week
                current_time = datetime.now().time()  # Get current time
                if timed_menu:
                    timed_menu_day = timed_menu.filter(dayofweek=current_day).first()

                    if timed_menu_day:
                    
                        if timed_menu_day.state == True:
                            start_time = timed_menu_day.start_time.strftime("%I:%M %p")

                            return start_time
                        else:
                            return None
                    else:
                            return None
                else:
                    return None
        def get_end_time(self, obj):
            if obj.is_timed == True:
                timed_menu = tbl_timedpromomenu.objects.filter(menutype=obj)
                current_day = datetime.now().strftime('%A')  # Get current day of the week
                current_time = datetime.now().time()  # Get current time
                if timed_menu:
                    timed_menu_day = timed_menu.filter(dayofweek=current_day).first()

                    if timed_menu_day:
                    
                        if timed_menu_day.state == True:
                            end_time = timed_menu_day.end_time.strftime("%I:%M %p")

                            return end_time
                        else:
                            return None
                    else:
                            return None
                else:
                    return None



        def to_representation(self, instance):
            representation = super().to_representation(instance)
            
            if instance.is_timed == True:
                timed_menu = tbl_timedpromomenu.objects.filter(menutype=instance)
                current_day = datetime.now().strftime('%A')  # Get current day of the week
                current_time = datetime.now().time()  # Get current time
                if timed_menu:
                    timed_menu_day = timed_menu.filter(dayofweek=current_day).first()

                    if timed_menu_day:
                    
                        if timed_menu_day.state == True:
                            start_time = timed_menu_day.start_time
                            end_time = timed_menu_day.end_time
                            
                            if  current_time >= start_time and current_time <= end_time:
                                menus = instance.menu_set.all()
                                serialized_menus = MenuSerializerList(menus, many=True).data
                            else:
                                print("The time is not met for seected timed menu")
                                menus = []
                                serialized_menus = []
                        else:
                            menus = instance.menu_set.all() 
                            serialized_menus = MenuSerializerList(menus, many=True).data  
                    else:
                            print("menu type does not have the appropriate day configuration")
                            menus = instance.menu_set.all() 
                            serialized_menus = MenuSerializerList(menus, many=True).data  
                else:
                    print("Menu type is not selected in the tbl timed")
                    menus = instance.menu_set.all() 
                    serialized_menus = MenuSerializerList(menus, many=True).data
            else:
                print("the menu type is not timed")
                # Serialize the menus related to this MenuType
                print(instance)
                menus = instance.menu_set.all()
                print(menus)
                serialized_menus = MenuSerializerList(menus, many=True).data

                print(f'{serialized_menus}serialized_menus')
            representation['products'] = serialized_menus
            
            return representation


class MenuTypeSerializerListOutletWise(serializers.ModelSerializer):
    products = MenuSerializerList(many=True, read_only=True) 
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = MenuType
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
        
    #     # Serialize the menus related to this MenuType
    #     menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
    #     serialized_menus = MenuSerializerList(menus, many=True, context=self.context).data
        
    #     representation['products'] = serialized_menus
        
    #     return representation

    def get_start_time(self, obj):
        if obj.is_timed == True:
            timed_menu = tbl_timedpromomenu.objects.filter(menutype=obj)
            current_day = datetime.now().strftime('%A')  # Get current day of the week
            current_time = datetime.now().time()  # Get current time
            if timed_menu:
                timed_menu_day = timed_menu.filter(dayofweek=current_day).first()

                if timed_menu_day:
                    
                    if timed_menu_day.state == True:
                        start_time = timed_menu_day.start_time.strftime("%I:%M %p")

                        return start_time
                    else:
                        return None
                else:
                        return None
            else:
                return None
    def get_end_time(self, obj):
        if obj.is_timed == True:
            timed_menu = tbl_timedpromomenu.objects.filter(menutype=obj)
            current_day = datetime.now().strftime('%A')  # Get current day of the week
            current_time = datetime.now().time()  # Get current time
            if timed_menu:
                timed_menu_day = timed_menu.filter(dayofweek=current_day).first()
                    
                if timed_menu_day:
                    
                    if timed_menu_day.state == True:
                        end_time = timed_menu_day.end_time.strftime("%I:%M %p")

                        return end_time
                    else:
                        return None
                else:
                        return None
            else:
                return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
            
        if instance.is_timed == True:
            timed_menu = tbl_timedpromomenu.objects.filter(menutype=instance)
            current_day = datetime.now().strftime('%A')  # Get current day of the week
            current_time = datetime.now().time()  # Get current time
            if timed_menu:
                timed_menu_day = timed_menu.filter(dayofweek=current_day).first()

                if timed_menu_day:
                    
                    if timed_menu_day.state == True:
                        start_time = timed_menu_day.start_time
                        end_time = timed_menu_day.end_time
                            
                        if  current_time >= start_time and current_time <= end_time:
                            menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
                            serialized_menus = MenuSerializerList(menus, many=True).data
                        else:
                            print("The time is not met for seected timed menu")
                            menus = []
                            serialized_menus = []
                    else:
                        menus = instance.menu_set.filter(outlet=self.context['outlet_name']) 
                        serialized_menus = MenuSerializerList(menus, many=True).data  
                else:
                        print("menu type does not have the appropriate day configuration")
                        menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
                        serialized_menus = MenuSerializerList(menus, many=True).data  
            else:
                print("Menu type is not selected in the tbl timed")
                menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
                serialized_menus = MenuSerializerList(menus, many=True).data
        else:
            print("the menu type is not timed")
            # Serialize the menus related to this MenuType
            print(instance)
            menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
            print(menus)
            serialized_menus = MenuSerializerList(menus, many=True).data

            print(f'{serialized_menus}serialized_menus')
        representation['products'] = serialized_menus
            
        return representation



# serializers.py

from rest_framework import serializers
from menu.models import MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['file', 'type']  # Adjust fields based on your requirements

from rest_framework import serializers
from menu.models import tbl_redeemproduct, TblRedeemedProduct

class TblRedeemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_redeemproduct
        exclude = [
                "created_at",
                "updated_at",
                "status",
                "is_deleted",
                "sorting_order",
                "is_featured"
            ]
            
class RedeemedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRedeemedProduct
        exclude = [
                "created_at",
                "updated_at",
                "status",
                "is_deleted",
                "sorting_order",
                "is_featured"
            ]
            
class RedeemedProductTodaySerializer(serializers.ModelSerializer):
    redeemed_productname = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    class Meta:
        model = TblRedeemedProduct
        exclude = [
                "updated_at",
                "status",
                "is_deleted",
                "sorting_order",
                "is_featured"
            ]
        
    def get_redeemed_productname(self, obj):
        return obj.redeemproduct.name
    
    def get_points(self, obj):
        return obj.redeemproduct.points
    
    def get_total(self, obj):
        return int(obj.quantity) * int(obj.redeemproduct.points)
        
from menu.models import tbl_timedpromomenu

class TimedPromoMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_timedpromomenu
        fields = ['id', 'menutype', 'dayofweek', 'start_time', 'end_time', 'state']
