from django.db import models
from root.utils import BaseModel

DAYS_OF_WEEK = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]

# Create your models here.
class tbl_discounts(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_timed = models.BooleanField(default=False)


class discountflag(BaseModel):
    discount = models.ForeignKey(tbl_discounts, models.CASCADE, null=True, blank=True)
    dayofweek = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    state = models.BooleanField(default=True)