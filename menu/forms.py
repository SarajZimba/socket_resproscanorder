from django import forms

from .models import Menu, MenuType, tbl_redeemproduct
from root.forms import BaseForm

# class MenuTypeForm(BaseForm, forms.ModelForm):
#     class Meta:
#         model = MenuType
#         fields = "__all__"
#         exclude = [
#             "is_deleted",
#             "status",
#             "deleted_at",
#             "sorting_order",
#             "slug",
#             "is_featured",
#         ]


class MenuForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Menu
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

    
class MenuTypeForm(BaseForm, forms.ModelForm):

    class Meta:
        model = MenuType
        fields = "__all__"
        exclude = [
            "is_deleted",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]
        
from organization.models import Organization

class OrganizationForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = [
            "is_deleted",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured"
        ]

class PointsOrganizationForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['loyalty_percentage', 'review_points']
        # exclude = [
        #     "is_deleted",
        #     "deleted_at",
        #     "sorting_order",
        #     "slug",
        #     "is_featured"
        # ]
     
from .models import MediaFile

class MediaFileForm(BaseForm, forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Menu.objects.filter(is_deleted=False))
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }   

class tbl_redeemproductForm(BaseForm, forms.ModelForm):

    class Meta:
        model = tbl_redeemproduct
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MenuitemID'] = forms.ModelChoiceField(queryset=Menu.objects.filter(is_deleted=False), required=False)
        self.fields["MenuitemID"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }

from .models import tbl_timedpromomenu

class TimedMenuForm(BaseForm, forms.ModelForm):
    class Meta:
        model = tbl_timedpromomenu
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]