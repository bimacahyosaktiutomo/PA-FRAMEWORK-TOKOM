from decimal import Decimal
from django.conf import settings
from tokom.models import Item 

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Create an empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, update_quantity=False):
        """
        Add an item to the cart or update its quantity.
        """
        item_id = str(item.item_id)  # Use item_id as the key
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(item.price),  # Convert to string for JSON serialization
                'name': item.name,  # Optional: store additional item info
                'image': item.image.url if item.image else None  # Optional
            }
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Save the cart in the session and mark it as modified.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, item):
        """
        Remove an item from the cart.
        """
        item_id = str(item.item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """
        Iterate over items in the cart and fetch items from the database.
        """
        item_ids = self.cart.keys()
        items = Item.objects.filter(item_id__in=item_ids)  # Fetch items from the database
        for item in items:
            self.cart[str(item.item_id)]['item'] = item

        for cart_item in self.cart.values():
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
