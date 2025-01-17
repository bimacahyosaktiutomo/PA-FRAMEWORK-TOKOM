import os
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Item, Category, Stock, OrderDetails, Order, Review
from .models.user_image import UserImage
from .forms import ItemForm, CartAddItemForm, UserForm, UserProfileForm, ReviewForm
from .cart import Cart

# cek apakah user memiliki akses
def is_Authorized(user):
    return user.groups.filter(name__in=['Worker', 'Admin']).exists() or user.is_superuser or user.is_staff

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Get the related image, or initialize it as None if it doesn't exist
    user_image = UserImage.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Handle old image removal if a new one is uploaded
            if request.FILES.get('image') and user_image and user_image.image:
                old_image_path = user_image.image.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('tokom:profile', user_id=user_id)
        else:
            messages.error(request, 'Failed to update profile.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'pages/profile.html', {
        'form': form,
        'user': user,
        'user_image': user_image,
    })

@login_required
def profile(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, id=user_id)
        # Get the related image, or initialize it as None if it doesn't exist
        user_image = UserImage.objects.filter(user=user).first()

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                # Handle old image removal if a new one is uploaded
                if request.FILES.get('image') and user_image and user_image.image:
                    old_image_path = user_image.image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('tokom:profile', user_id=user_id)
            else:
                messages.error(request, 'Failed to update profile.')
        else:
            form = UserProfileForm(instance=user)

        return render(request, 'pages/profile.html', {
            'form': form,
            'user': user,
            'user_image': user_image,
        })
    else:
        return redirect('tokom:home')


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
    elif dashboard_mode == 'reviews':
        context['reviews'] = Review.objects.all()
        template = 'dashboard/review.html'
    elif dashboard_mode == 'orders':
        context['orders'] = Order.objects.all()
        template = 'dashboard/order.html'
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
    user_image = UserImage.objects.filter(user=users).first()

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=users)
        if form.is_valid():
            if request.FILES.get('image') and user_image and user_image.image:
                old_image_path = user_image.image.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            new_password = form.cleaned_data.get('password')
            if new_password:
                users.set_password(new_password)  # Hash and save the new password
            form.save()
            messages.success(request, 'User berhasil diubah!')
            return redirect('tokom:dashboard', dashboard_mode='users')
        else:
            messages.error(request, 'User gagal diubah!')
    else:
        form = UserForm(instance=users)

    categories = Category.objects.all()
    return render(request, 'dashboard/edit_user.html', {'form': form, 'users' : users, 'user_image': user_image,})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # if request.method == 'POST':
    if not user.is_superuser:
        user.delete()
    else:
        JsonResponse({'success': False})
    return JsonResponse({'success': True})

# Display FRONTEND
from django.db.models import Avg
def homepage(request):
    categories = Category.objects.all()
    # items = Item.objects.all()
    items = Item.objects.annotate(average_rating=Avg('reviews__rating'))
    context = {
        'categories': categories,
        'items': items,
    }
    return render(request, 'homepage/index.html', context)

def product_details(request, item_id):
    item = Item.objects.get(item_id=item_id)
    reviews = Review.objects.filter(item=item)
    review_count = reviews.count()

    # Calculate the rating counts
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        rating_counts[review.rating] += 1

    # Calculate percentages for each rating
    rating_percentages = {}
    for rating in rating_counts:
        if review_count > 0:
            rating_percentages[rating] = (rating_counts[rating] / review_count) * 100
        else:
            rating_percentages[rating] = 0

    # Calculate the average rating
    total_reviews = reviews.count()
    if total_reviews > 0:
        average_rating = sum([review.rating for review in reviews]) / total_reviews
    else:
        average_rating = 0

    if request.user.is_authenticated:
        user = request.user
        reviews = sorted(reviews, key=lambda r: r.user != user)
    
    return render(
        request,
        "pages/product_details.html",
        {
            "item": item,
            'reviews': reviews,
            'review_count' : total_reviews,
            "rating_counts": rating_counts,
            "rating_percentages": rating_percentages,
            'average_rating': average_rating,
        },
    )

def search(request):
    query = request.GET.get('q', '')  # Search query
    queryCategories = request.GET.getlist('c')  # List of selected categories
    sort_by = request.GET.get('sort', '') # Sorting parameter
    items = Item.objects.annotate(average_rating=Avg('reviews__rating'))
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
def order_detail(request, order_id, mode = None):
    # Determine if the user is a staff member or regular user
    if request.user.is_staff:
        # Allow staff to access any order
        order = get_object_or_404(Order, pk=order_id)
    else:
        # Restrict regular users to their own orders
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
                    'total_item_price': item_data['total_item_price'],
                    'image_url': item.image.url if item.image else None,
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

    item = Item.objects.all
    if mode == None:
        return render(request, 'pages/order_detail.html', {
            'order': order,
            'items_data': items_data,
            'item' : item,
        })
    else:
        return render(request, 'dashboard/order_details.html', {
            'order': order,
            'items_data': items_data,
            'item' : item,
        })

@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status != 'Arrived':
        order.status = 'Arrived'
        order.date_arrived = now().date()  # Set the arrival date
        order.save()
        messages.success(request, "Order status has been updated to 'Finished' and arrival date recorded.")
    else:
        messages.info(request, "This order is already marked as finished.")

    return redirect('tokom:order_detail', order_id=order_id)

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status == 'Arrived' and order.status != 'Arrived':
            order.status = 'Arrived'
            order.date_arrived = now().date()  # Set the arrival date
            order.save()
            return JsonResponse({'success': True, 'message': "Order status updated to 'Arrived' and arrival date recorded."})
        
        elif new_status == 'Ongoing' and order.status != 'Ongoing':
            order.status = 'Ongoing'
            order.save()
            return JsonResponse({'success': True, 'message': "Order status updated to 'Ongoing'."})
        
        elif new_status == 'Package' and order.status != 'Package':
            order.status = 'Package'
            order.save()
            return JsonResponse({'success': True, 'message': "Order status updated to 'Package'."})

        return JsonResponse({'success': False, 'message': "No changes made to the order status."})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

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
def edit_review(request, review_id, item_id):
    review = get_object_or_404(Review, review_id=review_id)
    item = get_object_or_404(Item, pk=item_id)
    old_image = review.image
    
    # Ensure that the logged-in user is the one who created the review
    if review.user != request.user:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('tokom:product_details', item_id=review.item.item_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            if request.FILES:
                if old_image and os.path.isfile(str(old_image.path)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(old_image)))
            form.save()
            messages.success(request, "Your review has been updated!")
            return redirect('tokom:product_details', item_id=review.item.item_id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'pages/review_edit.html', {'form': form, 'review': review, 'item':item ,})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, review_id=review_id)
    
    # Ensure that the logged-in user is the one who created the review
    if review.user != request.user:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect('tokom:product_details', item_id=review.item.item_id)
    
    if request.method == 'POST':
        if review.image:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(review.image)))  # Adjust if necessary
            except Exception as e:
                messages.error(request, f'Error deleting image file: {e}')
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return JsonResponse({'success': True})
    return JsonResponse({'success': True})

# Cart
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
        print("Form is valid:", cd)  # Debugging line
        quantity = cd['quantity']
        update_quantity = cd['update']

        try:
            # Add or update the item in the cart, enforcing stock limits
            cart.add(item=item, quantity=quantity, update_quantity=update_quantity)
            messages.success(request, f"Added {quantity} x {item.name} to your cart.")
        except ValueError as e:
            # Handle stock limit error
            messages.error(request, str(e))
    else:
        messages.error(request, "Invalid form submission. Please try again.")
        print("Form is not valid:", form.errors)  # Debugging line  

    return redirect('tokom:cart')  # Redirect to the cart page

def cart_update(request, item_id):
    """
    View to update the quantity of an item in the cart via + or - actions.
    """
    cart = Cart(request)
    item = get_object_or_404(Item, item_id=item_id)

    # Get the action from the query parameters (?action=increase or ?action=decrease)
    action = request.GET.get('action')

    try:
        if action == "increase":
            cart.add(item=item, quantity=1, update_quantity=False)
            messages.success(request, f"Increased quantity of {item.name}.")
        elif action == "decrease":
            if cart.get_item_quantity(item_id) > 1:  # Ensure quantity doesn't drop below 1
                cart.add(item=item, quantity=-1, update_quantity=False)
                messages.success(request, f"Decreased quantity of {item.name}.")
            else:
                cart.remove(item)
                messages.success(request, f"Removed {item.name} from your cart.")
        else:
            messages.error(request, "Invalid action specified.")
    except ValueError as e:
        # Handle stock limit error
        messages.error(request, str(e))

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
        # email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')

        # if not address:
        #     messages.error(request, "Address is required.")
        #     return render(request, 'pages/checkout.html', {'cart': cart})

        # Validate stock availability for all items in the cart
        for item in cart:
            if item['quantity'] > item['item'].stock:
                messages.error(
                    request,
                    f"Not enough stock for {item['item'].name}. Only {item['item'].stock} left."
                )
                return render(request, 'pages/checkout.html', {'cart': cart})

        # Create the Order
        total_price = float(cart.get_total_price())  # Convert Decimal to float
        order = Order.objects.create(
            user=user,
            address=address,
            phone_number=phone_number,
            total_price=total_price,
            status='Ongoing'
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

            # Deduct stock for each item
            item['item'].stock -= item['quantity']
            item['item'].save()

        # Create the OrderDetails entry with all items and total price
        order_details = OrderDetails.objects.create(
            order=order,
            items=items,
            total_price=total_price
        )

        # Clear the cart and redirect
        cart.clear()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('tokom:order_success')

    # Pre-fill form with default address if available
    return render(request, 'pages/checkout.html', {'cart': cart})

def OrderSuccess(request):
    return render(request, 'pages/order_success.html')

# BUAT AG GRID
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer, UserSerializer, ReviewSerializer, OrderSerializer
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
    
class ReviewListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
class OrderListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
