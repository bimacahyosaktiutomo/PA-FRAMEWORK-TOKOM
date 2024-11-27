from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ItemListAPIView, UserListAPIView

app_name = 'tokom'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('search', views.search, name='search'),
    path('dashboard/<str:dashboard_mode>/', views.dashboard, name='dashboard'),
    path('profile', views.dashboard, name='profile'),
    path('product_details/<int:item_id>/', views.product_details, name='product_details'),
    
    # Item
    path('dashboard/items/add_item/', views.add_item, name='add_item'), 
    path('dashboard/items/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('dashboard/items/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),

    # User
    path('dashboard/users/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/users/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # path('cart/', views.cart, name='cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    
    # API
    path('api/items/' , ItemListAPIView.as_view(), name='item_list'),
    path('api/users/' , UserListAPIView.as_view(), name='user_list'),
]

# Biar bisa baca media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)