from django.urls import path
from api.views.branch import GetBranchImageView

urlpatterns = [
    # Your other URL patterns
    path('get-branch-image/<int:branch_id>/<int:terminal_no>/', GetBranchImageView.as_view(), name='get-branch-image'),
]