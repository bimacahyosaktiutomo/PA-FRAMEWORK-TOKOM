from django.contrib import admin
from django.urls import path
from . import views

app_name = 'tokom'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product_details/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
]