from product.models import Product
from collections import defaultdict
import json
# from order.utils import is_update_pending
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
def send_product_activedeactive_socket(product, outlet):
    channel_layer = get_channel_layer() 
    product_dict = {
        "title": product.title,
        "id": product.id,
        "slug": product.slug,
        "description": product.description,
        "image": product.image.url if product.image else None,
        "price": product.price,
        "is_taxable": product.is_taxable,
        "unit": product.unit,
        "barcode": product.barcode,
        "category": product.group,
        "reconcile": product.reconcile,
        "discount_exempt": product.discount_exempt,
        "type": product.type.title if product.type else None,
        "print_display": product.print_display,
        "isActive": product.status, 
        "is_billing_item":product.is_billing_item
    }

    group_name = f"product_group_{outlet}"
    async_to_sync(channel_layer.group_send)(
        group_name,  # The name of the group you're sending the message to
        {
            "type": "chat_message",
            "message": product_dict # The message you want to send
        }
    )