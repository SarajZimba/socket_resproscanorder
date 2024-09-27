import os
import django

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

# Setup Django
django.setup()

from product.models import Product
from menu.models import Menu

products = Product.objects.filter(is_deleted=False, status=True)

for product in products:
            Menu.objects.create(
                item_name=product.title,
                group=product.group,
                type=product.type.title,
                price=product.price,
                outlet='DMB',
                thumbnail = product.thumbnail,
                description=product.description if product.description else None,
                resproproduct= product,
                rating = product.rating,
                promotional_price = product.promotional_price,
                delete_check = product.delete_check,
                is_veg = product.is_veg,
                spice_level = product.spice_level,
                menutype = product.menutype
            )