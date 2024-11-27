from rest_framework import serializers

from .models.category import Category
from .models.item import Item
from .models.order_detail import OrderDetails
from .models.order import Order
from .models.review import Review
from .models.stock import Stock
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name'] 
    
class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = ['item_id', 'name', 'description', 'category' , 'rating', 'stock', 'discount', 'price', 'image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    item = ItemSerializer()

    class Meta:
        model = Review
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'