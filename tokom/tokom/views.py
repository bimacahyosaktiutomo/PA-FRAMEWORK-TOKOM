from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Category, Stock
from .forms import ItemForm

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

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard/dashboard.html')

@login_required
def dashboard(request):
    items = Item.objects.select_related('category').all()
    return render(request, 'dashboard/dashboard.html', {'items': items})

# ADD ITEM DI DASHBOARD
def add_item(request):
    # Check if categories exist; if not, create a default category
    if not Category.objects.exists():
        default_category = Category.objects.create(name="--------")

    items = Item.objects.all()

    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tokom:dashboard')  # Redirect after successful form submission
    else:
        form = ItemForm()

    categories = Category.objects.all()  # Fetch categories again if a new one was created
    return render(request, 'dashboard/add_item.html', {'form': form, 'items': items, 'categories': categories})

def delete_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('tokom:dashboard')
        
    return render(request, 'dashboard/delete_item.html', {'item': item})

