from django.shortcuts import render


from django.urls import reverse_lazy
from user.permission import IsAdminMixin, SearchMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
    TemplateView,

)

from .models import tbl_discounts

from root.utils import DeleteMixin


# Create your views here.
from django.http import JsonResponse
from .models import discountflag, tbl_discounts
from .forms import DiscountForm , DiscountTableForm
# from organization.models import Branch, EndDayRecord
# from .forms import BranchStockForm
class TimedDiscountMixin(IsAdminMixin):
    model = discountflag
    form_class = DiscountForm
    paginate_by = 10
    queryset = discountflag.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('timeddiscount_list')
    search_lookup_fields = [
        "product__item_name",
        "product__description",
    ]

class TimedDiscountList(TimedDiscountMixin, ListView):
    template_name = "scanpay/timeddiscount/timeddiscount_list.html"

class TimedDiscountDetail(TimedDiscountMixin, DetailView):
    template_name = "scanpay/timeddiscount/timeddiscount_detail.html"

class TimedDiscountCreate(TimedDiscountMixin, CreateView):
    template_name = "scanpay/timeddiscount/timeddiscount_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the menu types to the context
        context['discount_types'] = tbl_discounts.objects.filter(is_timed=True)
        context['days_of_week'] = [
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday')
        ]
        return context
    
    # def form_valid(self, form):
    #     if self.request.is_ajax():
    #         response_data = {
    #             'success': True,
    #             'redirect_url': reverse_lazy('Discount_list')
    #         }
    #         return JsonResponse(response_data)
    #     return super().form_valid(form)

class TimedDiscountUpdate(TimedDiscountMixin, UpdateView):
    template_name = "scanpay/update.html"

class TimedDiscountDelete(TimedDiscountMixin, DeleteMixin, View):
    pass

class DiscountTableMixin:
    model = tbl_discounts
    form_class = DiscountTableForm
    paginate_by = 10
    queryset = tbl_discounts.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('discounttable_list')

class DiscountTableList(DiscountTableMixin, ListView):
    template_name = "scanpay/discounttable/discounttable_list.html"
    queryset = tbl_discounts.objects.filter(status=True,is_deleted=False)

class DiscountTableDetail(DiscountTableMixin, DetailView):
    template_name = "scanpay/discounttable/discounttable_detail.html"

class DiscountTableCreate(DiscountTableMixin, CreateView):
    template_name = "scanpay/create.html"

class DiscountTableUpdate(DiscountTableMixin, UpdateView):
    template_name = "scanpay/update.html"

class DiscountTableDelete(DiscountTableMixin, DeleteMixin, View):
    pass
