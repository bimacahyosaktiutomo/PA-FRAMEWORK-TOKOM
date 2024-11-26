import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Item, Category, Stock, OrderDetail, Order, Review
from .forms import ItemForm, CartAddItemForm
from .cart import Cart

# cek apakah user memiliki akses
def is_Authorized(user):
    return user.groups.filter(name__in=['Worker', 'Admin']).exists() or user.is_superuser

def search(request):
    return render(request, 'pages/search.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

@login_required
def cart(request):
    return render(request, 'pages/cart.html')

# DASHBOARD
@login_required
@user_passes_test(is_Authorized)
def dashboard(request):
    items = Item.objects.select_related('category').all()
    return render(request, 'dashboard/dashboard.html', {'items': items})

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

# Display FRONTEND

def homepage(request):
    categories = Category.objects.all()
    items = Item.objects.all()
    context = {
        'categories': categories,
        'items': items,
    }
    return render(request, 'homepage/index.html', context)

def product_details(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    reviews = item.reviews.all()  # Use the 'reviews' related_name
    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'pages/product_details.html', context)

# CARTSSSSS
# @require_POST
# def cart_add(request, item_id):
#     """
#     View to add an item to the cart or update its quantity.
#     """
#     cart = Cart(request)
#     item = get_object_or_404(Item, item_id=item_id)
#     form = CartAddItemForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         print("Form is valid:", cd)  # Debugging line
#         cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
#     else:
#         print("Form is not valid:", form.errors)  # Debugging line
#     return redirect('tokom:cart')  # Replace with your cart detail view URL name

@require_POST
def cart_add(request, item_id):
    """
    View to add an item to the cart or update its quantity.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)  # Ensure you're getting the item correctly
    form = CartAddItemForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        print("Form is valid:", cd)  # Debugging line
        quantity = cd['quantity']
        update_quantity = cd['update']
        
        # Add or update the item in the cart
        cart.add(item=item, quantity=quantity, update_quantity=update_quantity)
        
        # Debugging to check if the item is added
        print(f"Item {item.name} added to cart with quantity {quantity}.")
    else:
        print("Form is not valid:", form.errors)  # Debugging line  
    return redirect('tokom:cart')  # Redirect to the cart page


def cart_remove(request, item_id):
    """
    View to remove an item from the cart.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)
    cart.remove(item)
    return redirect('tokom:cart')  # Replace with your cart detail view URL name

# def cart_detail(request):
#     """
#     View to display the cart and its contents.
#     """
#     cart = Cart(request)
#     for item in cart:
#         print(item)  # Debug the cart item
#         item['update_quantity_form'] = CartAddItemForm(initial={
#             'quantity': item['quantity'],
#             'update': True
#         })
#     return render(request, 'pages/cart.html', {'cart': cart})

def cart_detail(request):
    cart = Cart(request)
    # Debugging: Check if item.item exists and has item_id (your custom primary key)
    for cart_item in cart:
        item = cart_item.get('item')
        if item:
            print(f"Item ID: {item.item_id}, Item Name: {item.name}")  # Use item_id instead of id
        else:
            print(f"Item is missing for cart item {cart_item}")
    return render(request, 'pages/cart.html', {'cart': cart})

def order_create(request):
    """
    View to create an order from the cart.
    """
    cart = Cart(request)
    if request.method == "POST":
        # Create the order
        order = Order.objects.create(
            user=request.user,  # Assuming the user is logged in
            address=request.POST.get("address"),  # Collect address via form or POST
            total_price=cart.get_total_price(),
            status=False  # Default status as pending
        )

        # Create order details
        for item in cart:
            OrderDetail.objects.create(
                order=order,
                item=item['item'],
                quantity=item['quantity'],
                total_price=item['total_price']
            )

        # Clear the cart
        cart.clear()

        return redirect('order_success')  # Redirect to a success page

    return render(request, 'cart/checkout.html', {'cart': cart})

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
