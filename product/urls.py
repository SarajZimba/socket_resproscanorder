from . import views
from django.urls import path
urlpatterns = []

from .views import ProductCategoryList,ProductCategoryDetail,ProductCategoryCreate,ProductCategoryUpdate,ProductCategoryDelete,\
    ProductPointsCreate, ProductPointsDelete, ProductPointsDetail, ProductPointsUpdate,ProductPointsList
urlpatterns += [
path('prdct/category/', ProductCategoryList.as_view(), name='product_category_list'),
path('prdct/category/<int:pk>/', ProductCategoryDetail.as_view(), name='product_category_detail'),
path('prdct/category/create/', ProductCategoryCreate.as_view(), name='product_category_create'),
path('prdct/category/<int:pk>/update/', ProductCategoryUpdate.as_view(), name='product_category_update'),
path('prdct/category/delete', ProductCategoryDelete.as_view(), name='product_category_delete'),
]
               
from .views import ProductList,ProductDetail,ProductCreate,ProductUpdate,ProductDelete, ProductUploadView
urlpatterns += [
path('product/', ProductList.as_view(), name='product_list'),
path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
path('product/create/', ProductCreate.as_view(), name='product_create'),
path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
path('product/delete', ProductDelete.as_view(), name='product_delete'),
path('product/upload/', ProductUploadView.as_view(), name='product_upload'),


]

urlpatterns += [
    path('prdct/points/', ProductPointsList.as_view(), name='product_points_list'),
    path('prdct/points/<int:pk>/', ProductPointsDetail.as_view(), name='product_points_detail'),
    path('prdct/points/create/', ProductPointsCreate.as_view(), name='product_points_create'),
    path('prdct/points/<int:pk>/update/', ProductPointsUpdate.as_view(), name='product_points_update'),
    path('prdct/points/delete', ProductPointsDelete.as_view(), name='product_points_delete'),

]
               
from .views import CustomerProductList,CustomerProductDetail,CustomerProductCreate,CustomerProductUpdate,CustomerProductDelete
urlpatterns += [
path('prdct/client/', CustomerProductList.as_view(), name='customerproduct_list'),
path('prdct/client/<int:pk>/', CustomerProductDetail.as_view(), name='customerproduct_detail'),
path('prdct/client/create/', CustomerProductCreate.as_view(), name='customerproduct_create'),
path('prdct/client/<int:pk>/update/', CustomerProductUpdate.as_view(), name='customerproduct_update'),
path('prdct/client/delete', CustomerProductDelete.as_view(), name='customerproduct_delete'),
]

from .views import ProductStockList,ProductStockDetail,ProductStockCreate,ProductStockUpdate,ProductStockDelete
urlpatterns += [
path('stock/', ProductStockList.as_view(), name='productstock_list'),
path('stock/<int:pk>/', ProductStockDetail.as_view(), name='productstock_detail'),
path('stock/create/', ProductStockCreate.as_view(), name='productstock_create'),
path('stock/<int:pk>/update/', ProductStockUpdate.as_view(), name='productstock_update'),
path('stock/delete', ProductStockDelete.as_view(), name='productstock_delete'),
]

from .views import BranchStockList,BranchStockDetail,BranchStockCreate,BranchStockUpdate,BranchStockDelete, BranchStockUploadView, ReconcileView,\
    UpdateDateForReconcilationView
urlpatterns += [
path('bstck/', BranchStockList.as_view(), name='branchstock_list'),
path('bstck/<int:pk>/', BranchStockDetail.as_view(), name='branchstock_detail'),
path('bstck/create/', BranchStockCreate.as_view(), name='branchstock_create'),
path('bstck/<int:pk>/update/', BranchStockUpdate.as_view(), name='branchstock_update'),
path('bstck/delete', BranchStockDelete.as_view(), name='branchstock_delete'),
path('reconcile/', ReconcileView.as_view(), name='reconcile'),
path('bstck/upload-opening/', BranchStockUploadView.as_view(), name='branchstock_upload'),
path('update-date-reconcilation/', UpdateDateForReconcilationView.as_view(), name='update_date_reconcilation'),
]
  
from .views import ProductRecipieList,ProductRecipieDetail,ProductRecipieCreate,ProductRecipieUpdate
urlpatterns += [
    path('p-recipie/', ProductRecipieList.as_view(), name='productrecipie_list'),
    path('p-recipie/<int:pk>/', ProductRecipieDetail.as_view(), name='productrecipie_detail'),
    path('p-recipie/create/', ProductRecipieCreate.as_view(), name='productrecipie_create'),
    path('p-recipie/<int:pk>/update/', ProductRecipieUpdate.as_view(), name='productrecipie_update'),
    path('p-recipie/<int:pk>/delete', views.productrecipie_delete, name='productrecipie_delete'),
]
               