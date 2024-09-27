from django.db import models
from root.utils import BaseModel
from user.models import Customer
from django.db.models.signals import post_save
from organization.models import Branch
from django.dispatch import receiver

class ProductCategory(BaseModel):
    CATEGORY_CHOICES = (
        ("FOOD", "FOOD"),
        ("BEVERAGE", "BEVERAGE"),
        ("OTHERS", "OTHERS")
    )
    title = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="FOOD", verbose_name="Product Type", unique=True)
    slug = models.SlugField(unique=True, verbose_name="Category Slug")
    description = models.TextField(
        verbose_name="Description", null=True, blank=True
    )

    def __str__(self):
        return self.title

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Item Name", unique=True)
    slug = models.SlugField(unique=False, verbose_name="Item Slug")
    description = models.TextField(
        null=True, blank=True, verbose_name="Item Description"
    )
    unit = models.CharField(null=True, max_length=100, blank=True)
    
    is_taxable = models.BooleanField(default=True)
    cost_price = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="product/images/", null=True, blank=True)
    type = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, null=False, blank=False
    )
    group = models.CharField(max_length=20)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(null=True, max_length=100, blank=True)
    is_produced = models.BooleanField(default=False)
    reconcile = models.BooleanField(default=False)
    is_billing_item = models.BooleanField(default=False)
    discount_exempt = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
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
    menutype = models.ForeignKey(
        'menu.Menutype', on_delete=models.CASCADE, null=True, blank=True
    )
    
    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - Rs. {self.price} per {self.unit}"
        
    def save(self, *args, **kwargs):
        # Check if is_taxable is False and there is a taxbracket selected
        # if not self.is_taxable and self.taxbracket:
        #     self.taxbracket = None

        # if not self.thumbnail:  # Only generate thumbnail if it doesn't exist
        self.thumbnail = self.generate_thumbnail()

        super().save(*args, **kwargs)


    def generate_thumbnail(self, thumbnail_size=(100, 100)):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(thumbnail_size)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format='PNG')
            thumbnail_file = InMemoryUploadedFile(thumbnail_io, None, self.image.name.split('.')[0] + '_thumbnail.jpg', 'image/jpeg', thumbnail_io.tell(), None)
            thumbnail_file.seek(0)
            return thumbnail_file
        else:
            return None

        
@receiver(post_save, sender=Product)
def reverse_accounting_after_void(sender, instance, created, **kwargs):
    if created:
            from menu.models import Menu
            from organization.models import Organization
            Menu.objects.create(
                item_name=instance.title,
                group=instance.group,
                type=instance.type.title,
                price=instance.price,
                outlet=Organization.objects.last().org_name,
                thumbnail = instance.thumbnail,
                description=instance.description if instance.description else None,
                resproproduct= instance,
                rating = instance.rating,
                promotional_price = instance.promotional_price,
                delete_check = instance.delete_check,
                is_veg = instance.is_veg,
                spice_level = instance.spice_level,
                menutype = instance.menutype
            )
    else:
        from menu.models import Menu

        # Find all related Menu instances
        menus = Menu.objects.filter(resproproduct=instance)

        # Update each Menu instance with the new Product data
        for menu in menus:
            menu.item_name = instance.title
            menu.group = instance.group
            menu.type = instance.type.title if instance.type else ''
            menu.price = instance.price
            menu.thumbnail = instance.thumbnail
            menu.description = instance.description if instance.description else None,
            menu.rating = instance.rating
            menu.promotional_price = instance.promotional_price
            menu.delete_check = instance.delete_check
            menu.is_veg = instance.is_veg
            menu.spice_level = instance.spice_level
            menu.menutype = instance.menutype

            menu.save()

class ProductRecipie(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    items = models.JSONField()

    def __str__(self):
        return f'Recipies for {self.product.title}'


class RecipieItemSale(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # quantity = models.SmallIntegerField()
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    transaction_date = models.DateField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Recipie item sale'

class ProductStock(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    stock_quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.product.title} -> {self.stock_quantity}'

''' Signal to create ProductStock after Product instance is created '''


def create_stock(sender, instance, created, **kwargs):
    try:
        if not ProductStock.objects.filter(product=instance).exists() and created:
            ProductStock.objects.create(product=instance)
    except Exception as e:
        print(e)

post_save.connect(create_stock, sender=Product)


"""  ***********************  """



from django.contrib.auth import get_user_model

User = get_user_model()
class ProductMultiprice(models.Model):
    product_id = models.BigIntegerField()
    product_price = models.CharField(max_length=15)
    
    class Meta:
        managed = False
        db_table = 'product_multiprice'
    
    def __str__(self):
        return f"{self.product_id}- {self.product_price}"



class CustomerProduct(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.FloatField(default=0.0)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.title} - Rs. {self.price}"


class BranchStockTracking(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    opening = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    wastage = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    returned = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    sold = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    closing = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    physical = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    discrepancy = models.DecimalField(max_digits=10, decimal_places=3, default=0)


    def __str__(self):
        return f"{self.product.title}"
    
    class Meta:
        unique_together = "branch", "product", "date"


class BranchStock(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.title} to {self.branch.name}'
    
    def save(self, *args, **kwargs):
        if ProductStock.objects.filter(product=self.product).exists():
            product = ProductStock.objects.get(product=self.product)
            product.stock_quantity -= self.quantity
            product.save()
        return super().save(*args, **kwargs)
    

class ItemReconcilationApiItem(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    # wastage = models.IntegerField(default=0)
    # returned = models.IntegerField(default=0)
    # physical = models.IntegerField(default=0)
    wastage = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    returned = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    physical = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    terminal = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} -> {self.branch.name}"
    
    class Meta:
        unique_together = 'branch', 'product', 'date', 'terminal'
        
class ProductPoints(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"{self.product.title}"
        
class CustomerProductPointsTrack(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    starting_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    action = models.CharField(null=True, blank=True, max_length=20)
    remaining_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_no = models.CharField(max_length=255, null=True, blank=True)


