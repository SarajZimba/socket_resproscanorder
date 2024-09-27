
from django.urls import path
urlpatterns = []

from .views import MenuTypeList,MenuTypeDetail,MenuTypeCreate,MenuTypeUpdate,MenuTypeDelete

from .views import IndexView


urlpatterns = [
    path("index", IndexView.as_view(), name="scanpay_index"),
]


urlpatterns += [
path('menu/type/', MenuTypeList.as_view(), name='menu_type_list'),
path('menu/type/<int:pk>/', MenuTypeDetail.as_view(), name='menu_type_detail'),
path('menu/type/create/', MenuTypeCreate.as_view(), name='menu_type_create'),
path('menu/type/<int:pk>/update/', MenuTypeUpdate.as_view(), name='menu_type_update'),
path('menu/type/delete', MenuTypeDelete.as_view(), name='menu_type_delete'),

]

from .views import MenuList,MenuDetail,MenuCreate,MenuUpdate,MenuDelete, MenuUpload
urlpatterns += [
path('menu/', MenuList.as_view(), name='menu_list'),
path('menu/<int:pk>/', MenuDetail.as_view(), name='menu_detail'),
path('menu/create/', MenuCreate.as_view(), name='menu_create'),
path('menu/<int:pk>/update/', MenuUpdate.as_view(), name='menu_update'),
path('menu/delete', MenuDelete.as_view(), name='menu_delete'),
path('menu/upload/', MenuUpload.as_view(), name='menu_upload'),

]



from .views import MenuTypeProductList,MenuTypeProductCreate,MenuTypeProductDelete
# ,MenuTypeProductDetail,MenuTypeProductUpdate,
urlpatterns += [
path('menu_preset_product/<int:id>', MenuTypeProductList.as_view(), name='menu_preset_product_list'),
# path('menu_type_product/<int:pk>/', MenuTypeProductDetail.as_view(), name='menu_type_product_detail'),
path('menu_preset_product/create/<int:id>', MenuTypeProductCreate.as_view(), name='menu_preset_product_create'),
# path('menu_type_product/<int:pk>/update/', MenuTypeProductUpdate.as_view(), name='menu_type_product_update'),
path('menu_preset_product/remove/<int:id>/<int:menutype_id>', MenuTypeProductDelete.as_view(), name='menu_preset_product_remove'),

]

from .views import (
    OrganizationCreate,
    OrganizationDelete,
    OrganizationDetail,
    OrganizationUpdate,
)
urlpatterns += [
    path("organization/", OrganizationDetail.as_view(), name="organization_detail"),
    path(
        "organization/create/", OrganizationCreate.as_view(), name="organization_create"
    ),
    path(
        "organization/update/",
        OrganizationUpdate.as_view(),
        name="organization_update",
    ),
    path(
        "organization/delete", OrganizationDelete.as_view(), name="organization_delete"
    ),
]


from .views import FileList,FileDetail,FileCreate,FileUpdate,FileDelete
urlpatterns += [
path('product-file/', FileList.as_view(), name='file_list'),
# path('export_branch_stock/', export_branch_stock, name='export_branch_stock'),
path('product-file/<int:pk>/', FileDetail.as_view(), name='file_detail'),
path('product-file/create/', FileCreate.as_view(), name='file_create'),
path('product-file/<int:pk>/update/', FileUpdate.as_view(), name='file_update'),
path('product-file/delete', FileDelete.as_view(), name='file_delete'),



]


from .views import tbl_redeemproductList,tbl_redeemproductDetail,tbl_redeemproductCreate,tbl_redeemproductUpdate,tbl_redeemproductDelete
urlpatterns += [
path('tbl_redeemproduct/', tbl_redeemproductList.as_view(), name='tbl_redeemproduct_list'),
path('tbl_redeemproduct/<int:pk>/', tbl_redeemproductDetail.as_view(), name='tbl_redeemproduct_detail'),
path('tbl_redeemproduct/create/', tbl_redeemproductCreate.as_view(), name='tbl_redeemproduct_create'),
path('tbl_redeemproduct/<int:pk>/update/', tbl_redeemproductUpdate.as_view(), name='tbl_redeemproduct_update'),
path('tbl_redeemproduct/delete', tbl_redeemproductDelete.as_view(), name='tbl_redeemproduct_delete'),
# path('tbl_redeemproduct/upload/', tbl_redeemproductUpload.as_view(), name='tbl_redeemproduct_upload'),

]

from django.urls import path
from .views import CombinedView

urlpatterns += [
    path('combined/', CombinedView.as_view(), name='combined_view'),
]

from .views import TimedMenuList,TimedMenuDetail,TimedMenuCreate,TimedMenuUpdate,TimedMenuDelete
urlpatterns += [
path('timedmenu/', TimedMenuList.as_view(), name='timedmenu_list'),
# path('export_branch_stock/', export_branch_stock, name='export_branch_stock'),
path('timedmenu/<int:pk>/', TimedMenuDetail.as_view(), name='timedmenu_detail'),
path('timedmenu/create/', TimedMenuCreate.as_view(), name='timedmenu_create'),
path('timedmenu/<int:pk>/update/', TimedMenuUpdate.as_view(), name='timedmenu_update'),
path('timedmenu/delete', TimedMenuDelete.as_view(), name='timedmenu_delete'),
]