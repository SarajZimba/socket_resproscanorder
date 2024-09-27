from root.forms import BaseForm
from .models import MailRecipient
from django import forms

class MailRecipientForm(BaseForm, forms.ModelForm):
    class Meta:
        model = MailRecipient
        fields = '__all__'