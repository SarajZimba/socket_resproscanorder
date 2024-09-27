from .views import MailRecipientList,MailRecipientDetail,MailRecipientCreate,MailRecipientUpdate,MailRecipientDelete#, EndDayReportList
from django.urls import path


urlpatterns = [
path('mailrecipient/', MailRecipientList.as_view(), name='mailrecipient_list'),
path('mailrecipient/<int:pk>/', MailRecipientDetail.as_view(), name='mailrecipient_detail'),
path('mailrecipient/create/', MailRecipientCreate.as_view(), name='mailrecipient_create'),
path('mailrecipient/<int:pk>/update/', MailRecipientUpdate.as_view(), name='mailrecipient_update'),
path('mailrecipient/delete', MailRecipientDelete.as_view(), name='mailrecipient_delete'),
# path('endday-report/', EndDayReportList.as_view(), name='endday_report_list'),

]