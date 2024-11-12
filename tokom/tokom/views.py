from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'homepage/index.html')

def product_details(request):
    return render(request, 'pages/product_details.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')