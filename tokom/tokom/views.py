import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Item, Category, Stock, OrderDetail, Order, Review
from django.contrib.auth.models import User
from .forms import ItemForm, CartAddItemForm, UserForm
from .cart import Cart

# cek apakah user memiliki akses
def is_Authorized(user):
    return user.groups.filter(name__in=['Worker', 'Admin']).exists() or user.is_superuser

def search(request):
    query = request.GET.get('q', '')  # Search query
    queryCategories = request.GET.getlist('c')  # List of selected categories
    sort_by = request.GET.get('sort', '') # Sorting parameter
    items = Item.objects.all()
    categories = Category.objects.all()

    # Apply search filters
    filters = Q()
    if query:
        filters &= Q(name__icontains=query)  # Filter by name
    if queryCategories:
        # Combine category filters with OR logic
        category_filters = Q()
        for category in queryCategories:
            category_filters |= Q(category__name__icontains=category)
        filters &= category_filters

    items = items.filter(filters) if filters else items

    if sort_by:
        if sort_by == 'price_asc':
            items = items.order_by('price')  # Sort by price (ascending)
        elif sort_by == 'price_desc':
            items = items.order_by('-price')
        elif sort_by == 'default':
            items = items.filter(filters) if filters else items
        # elif sort_by == 'date_desc':
        #     items = items.order_by('-price')

    return render(request, 'pages/search.html', {
        'items': items,
        'category' : categories,
        'query': query,
        'queryCategory': queryCategories,
        'sort_by': sort_by,
    })

# def search(request):
#     query = request.GET.get('q')
#     queryCategory = request.GET.get('c')
#     items = Item.objects.all()
#     categories = Category.objects.all()
#     if query or queryCategory:
#         filters = Q()
#         if query:
#             filters &= Q(name__icontains=query)  # Add name filter if query exists
#         if queryCategory:
#             category_filters = Q()
#             for category in queryCategory:
#                 category_filters &= Q(category__name__icontains=category)
#             filters &= category_filters # Add category filter if queryCategory exists

#         items = items.filter(filters) if filters else items
#     return render(request, 'pages/search.html', {'items' : items, 'category' : categories, 'query' : query, 'queryCategory': queryCategory,})

def checkout(request):
    return render(request, 'pages/checkout.html')

@login_required
def cart(request):
    return render(request, 'pages/cart.html')

# DASHBOARD
@login_required
@user_passes_test(is_Authorized)
def dashboard(request, dashboard_mode):
    context = {}
    # Determine the mode and fetch the necessary data
    if dashboard_mode == 'items':
        context['items'] = Item.objects.select_related('category').all()
        template = 'dashboard/item.html'
    elif dashboard_mode == 'users':
        context['users'] = User.objects.all()
        template = 'dashboard/user.html'
    else:
        return render(request, '404.html', status=404)

    return render(request, template, context)

# Item
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
            return redirect('tokom:dashboard', dashboard_mode='items')
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
            return redirect('tokom:dashboard', dashboard_mode='items')
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

# User
def edit_user(request, id):
    users = get_object_or_404(User, id=id)
    # old_image = users.image

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diubah!')
            return redirect('tokom:dashboard', dashboard_mode='users')
        else:
            messages.error(request, 'Produk gagal diubah!')
    else:
        form = UserForm(instance=users)

    categories = Category.objects.all()
    return render(request, 'dashboard/edit_user.html', {'form': form, 'users' : users})

def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    # if request.method == 'POST':
    user.delete()
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
@require_POST
def cart_add(request, item_id):
    """
    View to add an item to the cart or update its quantity.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('tokom:cart')  # Replace with your cart detail view URL name

def cart_remove(request, item_id):
    """
    View to remove an item from the cart.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)
    cart.remove(item)
    return redirect('tokom:cart')  # Replace with your cart detail view URL name

def cart_detail(request):
    """
    View to display the cart and its contents.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddItemForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
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
from .serializers import ItemSerializer, UserSerializer
from django.contrib.auth.models import User

class ItemListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class UserListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)