from rest_framework import serializers

from .models.category import Category
from .models.item import Item
from .models.order_detail import OrderDetails
from .models.order import Order
from .models.review import Review
from .models.stock import Stock


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name'] 
    
class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = ['item_id', 'name', 'description', 'category' , 'rating', 'stock', 'discount', 'price', 'image']