from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
# Create your views here.

from .models import MailRecipient
from .forms import MailRecipientForm
from django.http import JsonResponse


class MailRecipientMixin:
    model = MailRecipient
    form_class = MailRecipientForm
    paginate_by = 10
    queryset = MailRecipient.objects.filter(status = True)
    success_url = reverse_lazy('mailrecipient_list')

class MailRecipientList(MailRecipientMixin, ListView):
    template_name = "mailrecipient/mailrecipient_list.html"
    queryset = MailRecipient.objects.filter(status=True)

class MailRecipientDetail(MailRecipientMixin, DetailView):
    template_name = "mailrecipient/mailrecipient_detail.html"

class MailRecipientCreate(MailRecipientMixin, CreateView):
    template_name = "create.html"

class MailRecipientUpdate(MailRecipientMixin, UpdateView):
    template_name = "update.html"

class MailRecipientDelete(MailRecipientMixin, View):

    def remove_from_DB(self, request):
        try:
            print("Object deleted")
            object_id = request.GET.get("pk", None)
            object = self.model.objects.get(id=object_id)
            object.status = False
            object.save()
            return True
        except Exception as e:
            print(e)
            return str(e)
        
    def get(self, request):
        status = self.remove_from_DB(request)
        return JsonResponse({"deleted": status})