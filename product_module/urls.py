from django.urls import path
from . import views

urlpatterns = [
    # path('<cat>/', views.ProductListView.as_view(), name='product_list_page'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('<cat>/', views.ProductListView.as_view(), name='product_list_page'),
    path('<cat>/<slug>/', views.ProductDetailView.as_view(), name='product_detail_page'),

]