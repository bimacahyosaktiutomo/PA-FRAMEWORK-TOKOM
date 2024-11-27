import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Item, Category, Stock, OrderDetails, Order, Review
from .forms import ItemForm, CartAddItemForm, UserForm, ReviewForm
from .cart import Cart

# cek apakah user memiliki akses
def is_Authorized(user):
    return user.groups.filter(name__in=['Worker', 'Admin']).exists() or user.is_superuser

# @login_required
# def cart(request):
#     return render(request, 'pages/cart.html')

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
def edit_user(request, user_id):
    users = get_object_or_404(User, id=user_id)
    # old_image = users.image

    if request.method == 'POST':
        form = UserForm(request.POST, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'User berhasil diubah!')
            return redirect('tokom:dashboard', dashboard_mode='users')
        else:
            messages.error(request, 'User gagal diubah!')
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
    
    # Calculate the average rating
    total_reviews = reviews.count()
    if total_reviews > 0:
        average_rating = sum([review.rating for review in reviews]) / total_reviews
    else:
        average_rating = 0
    context = {
        'item': item,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': total_reviews,
    }
    return render(request, 'pages/product_details.html', context)

# def product_details(request, item_id):
#     item = Item.objects.get(item_id=item_id)
#     reviews = Review.objects.filter(item=item)

#     # Calculate the average rating
#     total_reviews = reviews.count()
#     if total_reviews > 0:
#         average_rating = sum([review.rating for review in reviews]) / total_reviews
#     else:
#         average_rating = 0

#     # Calculate rating distribution (how many 5-star, 4-star, etc. reviews)
#     rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
#     for review in reviews:
#         rating_distribution[review.rating] += 1

#     # Prepare context for the template
#     context = {
#         'item': item,
#         'average_rating': average_rating,
#         'review_count': total_reviews,
#         'rating_distribution': rating_distribution,
#     }
    
#     return render(request, 'pages/product_details.html', context)

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
    
# Order history & review
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_id')
    return render(request, 'pages/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_details = order.order_details.all()

    # Parse items from JSON and retrieve corresponding Item instances
    items_data = []
    for detail in order_details:
        for item_data in detail.items:  # Iterate through the list in JSONField
            try:
                item = Item.objects.get(pk=item_data['item_id'])
                items_data.append({
                    'item': item,
                    'item_name': item_data['item_name'],
                    'price_per_item': item_data['price_per_item'],
                    'quantity': item_data['quantity'],
                    'total_item_price': item_data['total_item_price']
                })
            except Item.DoesNotExist:
                # Handle the case where an item_id in the JSON is not in the database
                items_data.append({
                    'item': None,
                    'item_name': item_data['item_name'],
                    'price_per_item': item_data['price_per_item'],
                    'quantity': item_data['quantity'],
                    'total_item_price': item_data['total_item_price']
                })

    return render(request, 'pages/order_detail.html', {
        'order': order,
        'items_data': items_data,
    })

@login_required
def create_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')
        Review.objects.create(user=request.user, item=item, review_text=review_text, rating=rating, image=image)
        return redirect('tokom:product_details', item_id=item_id)
    return render(request, 'pages/review_create.html', {'item': item})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, review_id=review_id)
    
    # Ensure that the logged-in user is the one who created the review
    if review.user != request.user:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('tokom:product_details', item_id=review.item.item_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated!")
            return redirect('tokom:product_details', item_id=review.item.item_id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'pages/review_edit.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, review_id=review_id)
    
    # Ensure that the logged-in user is the one who created the review
    if review.user != request.user:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect('tokom:product_details', item_id=review.item.item_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('tokom:product_details', item_id=review.item.item_id)

    return render(request, 'pages/review_delete.html.html', {'review': review})

# CARTSSSSS
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

def cart_update(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)

    # Get the action from the query parameters (?action=increase or ?action=decrease)
    action = request.GET.get('action')

    if action == "increase":
        cart.add(item=item, quantity=1, update_quantity=False)
    elif action == "decrease":
        if cart.get_item_quantity(item_id) > 1:  # Ensure quantity doesn't drop below 1
            cart.add(item=item, quantity=-1, update_quantity=False)
        else:
            cart.remove(item)  # Remove item if quantity drops to zero

    # # Optionally handle AJAX responses
    # if request.is_ajax():
    #     return JsonResponse({
    #         'quantity': cart.get_item_quantity(item_id),
    #         'total_price': cart.get_total_price(),
    #     })

    return redirect('tokom:cart')

def cart_remove(request, item_id):
    """
    View to remove an item from the cart.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)
    cart.remove(item)
    return redirect('tokom:cart')  # Replace with your cart detail view URL name

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

@login_required
def checkout(request):
    user = request.user
    cart = Cart(request)

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if not address:
            return render(request, 'pages/checkout.html', {'cart': cart, 'error': "Address is required."})

        # Create the Order
        total_price = float(cart.get_total_price())  # Convert Decimal to float

        order = Order.objects.create(
            user=user,
            address=address,
            total_price=total_price,
            status=False
        )

        # Create OrderDetails with item details (name, id, price per item, etc.)
        items = []
        for item in cart:
            items.append({
                'item_id': item['item'].item_id,
                'item_name': item['item'].name,
                'price_per_item': float(item['item'].price),  # Convert Decimal to float
                'quantity': item['quantity'],
                'total_item_price': float(item['total_price'])  # Convert Decimal to float
            })

        # Create the OrderDetails entry with all items and total price
        order_details = OrderDetails.objects.create(
            order=order,
            items=items,
            total_price=total_price
        )

        # Clear the cart and redirect
        cart.clear()
        return redirect('tokom:home')

    # Pre-fill form with default address if available
    return render(request, 'pages/checkout.html', {'cart': cart})

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