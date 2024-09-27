from django import forms
from root.forms import BaseForm


from .models import discountflag

class DiscountForm(BaseForm, forms.ModelForm):
    class Meta:
        model = discountflag
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]


from django import forms

from .models import tbl_discounts

class DiscountTableForm(BaseForm, forms.ModelForm):
    class Meta:
        model = tbl_discounts
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','discount_type', 'is_featured', 'sorting_order']
                        