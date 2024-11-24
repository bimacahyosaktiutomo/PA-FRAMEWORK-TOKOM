from django.contrib import admin
from django.urls import path
from . import views

app_name = 'tokom'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('search', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product_details/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/add_item/', views.add_item, name='add_item'), #ADD ITEM DI DASHBOARD
    path('dashboard/edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('dashboard/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]