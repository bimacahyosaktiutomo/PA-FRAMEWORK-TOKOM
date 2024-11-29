from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ItemListAPIView, UserListAPIView , ReviewListAPIView, OrderListAPIView

app_name = 'tokom'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('search', views.search, name='search'),
    path('dashboard/<str:dashboard_mode>/', views.dashboard, name='dashboard'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('product_details/<int:item_id>/', views.product_details, name='product_details'),
    
    # Item
    path('dashboard/items/add_item/', views.add_item, name='add_item'), 
    path('dashboard/items/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('dashboard/items/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),

    # User
    path('dashboard/users/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/users/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Pembelian
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.OrderSuccess, name='order_success'),
    
    # Order history & Review
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('dashboard/orders/<int:order_id>/<str:mode>/', views.order_detail, name='order_detail'),
    path('order_status_change/<int:order_id>/', views.change_order_status, name='order_status_change'),
    path('items/<int:item_id>/review/', views.create_review, name='create_review'),
    path('reviews/edit/<int:item_id>/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    
    # API
    path('api/items/' , ItemListAPIView.as_view(), name='item_list'),
    path('api/users/' , UserListAPIView.as_view(), name='user_list'),
    path('api/reviews/' , ReviewListAPIView.as_view(), name='review_list'),
    path('api/orders/' , OrderListAPIView.as_view(), name='order_list'),
    path('api/reviews/' , ReviewListAPIView.as_view(), name='review_list'),
    path('api/orders/' , OrderListAPIView.as_view(), name='order_list'),
]

# Biar bisa baca media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)