from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'homepage/index.html')

def search(request):
    return render(request, 'pages/search.html')

def product_details(request):
    return render(request, 'pages/product_details.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

@login_required
def cart(request):
    return render(request, 'pages/cart.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')