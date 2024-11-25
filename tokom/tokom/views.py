import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Item, Category, Stock
from .forms import ItemForm


# cek apakah user memiliki akses
def is_Authorized(user):
    return user.groups.filter(name__in=['Worker', 'Admin']).exists() or user.is_superuser

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
@user_passes_test(is_Authorized)
def dashboard(request):
    items = Item.objects.select_related('category').all()
    return render(request, 'dashboard/dashboard.html', {'items': items})

# ADD ITEM DI DASHBOARD
def add_item(request):
    # Check if categories exist
    if not Category.objects.exists():
        default_category = Category.objects.create(name="--------")

    items = Item.objects.all()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambah!')
            return redirect('tokom:dashboard')
        else:
            messages.error(request, 'Produk gagal ditambah!')
    else:
        form = ItemForm()

    categories = Category.objects.all()
    return render(request, 'dashboard/add_item.html', {'form': form, 'items' : items, 'categories': categories})

def edit_item(request, item_id):
    items = get_object_or_404(Item, item_id=item_id)
    old_image = items.image

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=items)
        if form.is_valid():
            if request.FILES:
                if old_image and os.path.isfile(str(old_image.path)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(old_image)))
            form.save()
            messages.success(request, 'Produk berhasil diubah!')
            return redirect('tokom:dashboard')
        else:
            messages.error(request, 'Produk gagal diubah!')
    else:
        form = ItemForm(instance=items)

    categories = Category.objects.all()
    return render(request, 'dashboard/edit_item.html', {'form': form, 'items' : items, 'categories': categories})

def delete_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    # if request.method == 'POST':
    if item.image:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(item.image)))  # Adjust if necessary
        except Exception as e:
            messages.error(request, f'Error deleting image file: {e}')
    item.delete()
    return JsonResponse({'success': True})

# BUAT AG GRID
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class ItemListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    

# AG GRID FILTERING

from django.core.paginator import Paginator
from django.http import JsonResponse

def items_api(request):
    items = Item.objects.all()

    # Handle filtering
    name_filter = request.GET.get('name_filter', '')
    if name_filter:
        items = items.filter(name__icontains=name_filter)

    category_filter = request.GET.get('category_filter', '')
    if category_filter:
        items = items.filter(category__name__icontains=category_filter)

    # Handle sorting
    sort_field = request.GET.get('sortField', 'id')
    sort_order = request.GET.get('sortOrder', 'asc')
    if sort_order == 'desc':
        sort_field = f"-{sort_field}"
    items = items.order_by(sort_field)

    # Handle pagination
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 100))
    paginator = Paginator(items, end - start)
    page = paginator.get_page(start // paginator.per_page + 1)

    rows = list(page.object_list.values(
        "id", "name", "category__name", "price", "stock"
    ))
    return JsonResponse({
        "rows": rows,
        "totalCount": paginator.count,
    })
