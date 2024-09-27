from django.db import models
from root.utils import BaseModel
import json
from user.models import Customer
from discounts.models import tbl_discounts

# Create your models here.

class ScanPayOrder(BaseModel):
    employee = models.CharField(max_length=155, null=True)
    table_no = models.IntegerField(null=True)
    noofguest = models.IntegerField(null=True)
    start_time = models.CharField(max_length=255,null=True)
    end_time = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255, null=True)    
    discounts = models.ForeignKey(tbl_discounts, models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True)
    barItem = models.CharField(max_length=10, null=True) 
    outlet = models.CharField(max_length = 100, null=True)
    accepted_time = models.CharField(max_length=100, null=True)
    outlet_order = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, models.CASCADE, null=True, blank=True)
    billreqwithdiscount = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True)


class ScanPayOrderDetails(BaseModel):
    order = models.ForeignKey(ScanPayOrder, null=True, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=200, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currentState = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(null=True)
    modification = models.CharField(max_length=200, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)


from django.db.models.signals import post_save
from user.models import UserLogin
from django.dispatch import receiver
from .firebase import send_notification
            
            
class BillRequest(BaseModel):
    table_no = models.IntegerField()
    is_billrequest = models.BooleanField(default=False)
    is_waitercalling = models.BooleanField(default=False)
    outlet = models.CharField(max_length = 100, null=True)
    completed_time = models.CharField(max_length=100, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    order = models.OneToOneField(ScanPayOrder, models.CASCADE, null=True, blank=True)

from user.models import UserBranchLogin
from order.utils import get_terminal
@receiver(post_save, sender=BillRequest)
def send_delivery_notification(sender, instance, created, **kwargs):
    print("I am inside")
    if created:
        outlet=instance.outlet
        from organization.models import Branch
        branch=Branch.objects.filter(branch_code=outlet, is_deleted=False, status=True).first()
        active_users = UserBranchLogin.objects.filter(branch=branch)

        start_time = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        if active_users:
            for user in active_users:

                is_billrequest = instance.is_billrequest if instance.is_billrequest else ""
                billrequest_id = instance.id 

                table_no = instance.table_no if instance.table_no else ""
                terminal = get_terminal(branch, table_no)
                is_waitercalling = instance.is_waitercalling if instance.is_waitercalling else ""
                # employee = instance.employee if instance.employee else ""
                start_time = start_time 
                token = user.device_token
                # outlet = instance.outlet if instance.outlet else "" 

                order_dict = {}

                if billrequest_id is not None:
                    order_dict["billrequest_id"] = str(billrequest_id)
                            
                if is_billrequest is not None:
                    order_dict["is_billrequest"] = str(is_billrequest)
                                
                if is_waitercalling is not None:
                    order_dict["is_waitercalling"] = str(is_waitercalling)

                if table_no is not None:
                    order_dict["tableNo"] = str(table_no)

                if start_time is not None:
                    order_dict["start_time"] = str(start_time)

                if terminal is not None:
                    order_dict["terminal"] = str(terminal)

                final_msg = ""
                if instance.is_billrequest == True:
                    final_msg = f"You have a new bill request from table no {str(table_no)} "
                if instance.is_waitercalling == True:
                    final_msg = f"You have a waiter request from table no {str(table_no)}"

                if token is not None or token != '':
                    print(f"before {order_dict}")
                    send_notification(token, "New request received", final_msg, order_dict)
                    print(f"after {order_dict}")
                else:
                    print("The token is None")
        else:
            print(f"No active users in the outlet {outlet}")
            
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
class HashValue(BaseModel):
    outlet = models.CharField(max_length=100, null=True, blank=True)
    table = models.IntegerField()
    hash_value = models.CharField(max_length=64, blank=True, null=True) 

    def save(self, *args, **kwargs):
        self.hash_value = self.generate_hash()
        super().save(*args, **kwargs)

    def generate_hash(self):
        hash_object = hashlib.sha256()
        hash_object.update(f"{self.outlet}{self.table}".encode('utf-8'))
        return hash_object.hexdigest()

@receiver(post_save, sender=HashValue)
def update_hash_value(sender, instance, created, **kwargs):
    if created:
        instance.hash_value = instance.generate_hash()
        instance.save()