from django import forms
from django.forms.models import inlineformset_factory
from root.forms import BaseForm  # optional

from .models import ProductCategory, ProductPoints


class ProductCategoryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]


from .models import Product
from datetime import time

class ProductForm(BaseForm, forms.ModelForm):
    average_prep_time_minutes = forms.IntegerField(
        required=False,
        label="Average Prep Time (minutes)",
        help_text="Enter the average preparation time in minutes."
    )
    class Meta:
        model = Product
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "thumbnail",
            "description",
            "product_id",
            # "average_prep_time"
        ]
    def save(self, commit=True):
        product = super().save(commit=False)

        minutes = self.cleaned_data.get('average_prep_time_minutes')
        print(f"Minutes input: {minutes}")  # Debugging line
        if minutes is not None and minutes >= 0:    
            hours = minutes // 60
            minutes = minutes % 60
            product.average_prep_time = time(hour=hours, minute=minutes)
            print(f"Saving average_prep_time as: {product.average_prep_time}")  # Debugging line
        else:
            product.average_prep_time = None

        if commit:
            product.save()
        return product


from .models import CustomerProduct


class CustomerProductForm(BaseForm, forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "agent",
        ]

from .models import ProductStock

class ProductStockForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]


from .models import BranchStock
class BranchStockForm(BaseForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.all())
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }

    class Meta:
        model = BranchStock
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','sorting_order', 'is_featured']
        
from .models import ProductRecipie

class ProductRecipieForm(BaseForm, forms.ModelForm):
    items = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), required=False)
    class Meta:
        model = ProductRecipie
        fields = 'product', 'instruction'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }
        self.fields["items"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Recipe Item",
                        }

class ProductPointsForm(BaseForm, forms.ModelForm):

    class Meta:
        model = ProductPoints
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]
        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-control": "select2",
                    "data-placeholder": "Select Product",
                }
            ),
        }


class ProductPointsUpdateForm(BaseForm, forms.ModelForm):

    class Meta:
        model = ProductPoints
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "product"
        ]


from .models import tblModifications

class tblModificationsForm(BaseForm, forms.ModelForm):
    class Meta:
        model = tblModifications
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]