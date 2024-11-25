from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ItemListAPIView

app_name = 'tokom'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('search', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product_details/<int:item_id>/', views.product_details, name='product_details'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('dashboard/add_item/', views.add_item, name='add_item'), 
    path('dashboard/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('dashboard/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    
    # path('cart/', views.cart, name='cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # API
    path('api/items/' , ItemListAPIView.as_view(), name='item_list'),
]

# Biar bisa baca media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)