from django.urls import path

from api.views.end_day import EndDayDailyReportFilterView, MasterEndDay, BranchTotalEndDay, LastTerminalCheck, MailCheck, BranchTodaysSalesDateWise

urlpatterns = [
    # Other URL patterns...
    path('endday-reports/<int:branch_id>/', EndDayDailyReportFilterView.as_view(), name='endday-reports'),
    path('master-endday-mail/', MasterEndDay.as_view(), name='master-endday'),

    path('branch-endday-total/', BranchTotalEndDay.as_view(), name='branch-enddaytotals' ),
    path('branch-total-todayssales/', BranchTodaysSalesDateWise.as_view(), name='branch-total-todayssales' ),
    path('lastterminal-check/<str:terminal_no>', LastTerminalCheck.as_view(), name='branch-enddaytotals' )

]
urlpatterns += [
    # Other URL patterns...

    path('mail-check-single/', MailCheck.as_view(), name='mail-check-single' )

]

