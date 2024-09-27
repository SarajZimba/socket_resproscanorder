from root.utils import BaseModel
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product
# Create your models here.

class MenuType(BaseModel):
    title = models.CharField(max_length=255, verbose_name="MenuType Title", unique=True)
    slug = models.SlugField(verbose_name="MenuType Slug", null=True)
    description = models.TextField(
        verbose_name="MenuType Description", null=True, blank=True
    )
    is_timed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Menu(BaseModel):
    item_name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="Product Slug", null=True)
    group = models.CharField(max_length=255)   
    type = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    outlet = models.CharField(max_length=255)
    discount_exempt = models.BooleanField(default=False)
    is_promotional = models.BooleanField(default=False)
    is_todayspecial = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    image_bytes = models.TextField(null=True, blank=True)
    menutype = models.ForeignKey(
        MenuType, on_delete=models.CASCADE, null=True, blank=True
    )
    description =models.TextField(null=True, blank=True)
    # respro_itemId = models.IntegerField(null=True, blank=True)
    # resproproductId = models.ForeignKey(Product, models.CASCADE, null=True, blank=True)
    resproproduct = models.OneToOneField(Product, models.CASCADE, null=True, blank=True)
    
    rating_choices = (
        (0.0, '0.0'),
        (0.5, '0.5'),
        (1.0, '1'),
        (1.5, '1.5'),
        (2.0, '2'),
        (2.5, '2.5'),
        (3.0, '3'),
        (3.5, '3.5'),
        (4.0, '4'),
        (4.5, '4.5'),
        (5.0, '5'),
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=rating_choices, default=0.0)
    promotional_price = models.FloatField(default=0.0)    
    delete_check = models.BooleanField(default=True)
    is_veg = models.BooleanField(null=True, blank=True)

    spice_choices = (
            (1.0, '1'),
            (2.0, '2'),
            (3.0, '3'),
            (4.0, '4'),
            (5.0, '5'),
        )
    spice_level = models.DecimalField(max_digits=2, decimal_places=1, choices=spice_choices, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.item_name}"

    def save(self, *args, **kwargs):
        self.thumbnail = self.generate_thumbnail()

        #This is to generate the slug for sending it in the api
        self.slug = slugify(self.item_name)


        super().save(*args, **kwargs)

    def generate_thumbnail(self, thumbnail_size=(300, 300)):
        if self.thumbnail:
            image = Image.open(self.thumbnail)
            image.thumbnail(thumbnail_size)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format='PNG')
            thumbnail_file = InMemoryUploadedFile(thumbnail_io, None, self.thumbnail.name.split('.')[0] + '_thumbnail.jpg', 'image/jpeg', thumbnail_io.tell(), None)
            thumbnail_file.seek(0)
            return thumbnail_file
        else:
            return None
        
class FlagMenu(models.Model):
    use_same_menu_for_multiple_outlet = models.BooleanField(default=True)
    autoaccept_order = models.BooleanField(default=False)
    send_payload_in_notification = models.BooleanField(default=False)
    allow_discount = models.BooleanField(default=False)


class Organization(BaseModel):
    name = models.CharField(max_length = 100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    org_logo = models.ImageField(
        upload_to="organization/images/", null=True, blank=True
    )
    loyalty_percentage = models.FloatField(default=0.0)
    review_points = models.FloatField(default=0.0)
    background_image = models.ImageField(upload_to="organization/images", null=True, blank=True)

    def __str__(self):
        return self.name

class MediaFile(BaseModel):
    product = models.ForeignKey(Menu, related_name='media_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media_files/', null=True)
    type = models.CharField(max_length=44, null=True, blank=True)
    def get_file_type(self):
        if self.file:
            file_type = self.file.file.content_type
            return file_type
        return None

    def is_image(self):
        file_type = self.get_file_type()
        return file_type and file_type.startswith('image/')

    def is_video(self):
        file_type = self.get_file_type()
        return file_type and file_type.startswith('video/')
    
    def save(self, *args, **kwargs):
        # Set the type field based on file type before saving
        if self.file:
            if self.is_image():
                self.type = 'image'
            elif self.is_video():
                self.type = 'video'
            else:
                self.type = 'unknown' 

        super().save(*args, **kwargs)

    def __str__(self):
        return f"File for {self.product.item_name}"
        
class tbl_redeemproduct(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    points = models.FloatField(default=0.0)
    group = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    state = models.BooleanField(default=True)
    is_Menuitem = models.BooleanField(default=False)
    image = models.ImageField(upload_to='redeemproduct/', blank=True, null=True)
    MenuitemID = models.ForeignKey(Menu, models.CASCADE, null=True, blank=True)
    
from user.models import Customer
from order.models import ScanPayOrder
class TblRedeemedProduct(BaseModel):
    redeemproduct = models.ForeignKey(tbl_redeemproduct, models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Customer, models.CASCADE, null=True, blank=True)
    outlet = models.CharField(max_length=100, null=True, blank=True)
    order = models.ForeignKey(ScanPayOrder, models.CASCADE, null=True, blank=True)
    state = models.CharField(default="Pending", max_length=255, null=True)
    

DAYS_OF_WEEK = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]
    
class tbl_timedpromomenu(BaseModel):
    menutype = models.ForeignKey(MenuType, models.CASCADE, null=True, blank=True)
    dayofweek = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    state = models.BooleanField(default=True)

