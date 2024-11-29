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
        
        # Calculate the new quantity
        new_quantity = quantity if update_quantity else self.cart[item_id]['quantity'] + quantity
        
        # Validate stock availability
        if new_quantity > item.stock:
            raise ValueError(f"Cannot add more than {item.stock} units of {item.name} to the cart.")
        
        # Update quantity if valid
        if new_quantity > 0:
            self.cart[item_id]['quantity'] = new_quantity
        else:
            self.remove(item)

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

    def get_item_quantity(self, item_id):
        """Get the quantity of a specific item in the cart."""
        return self.cart[str(item_id)]['quantity'] if str(item_id) in self.cart else 0
    
    def __iter__(self):
        """
        Iterate over items in the cart and fetch items from the database.
        """
        item_ids = self.cart.keys()
        items = Item.objects.filter(item_id__in=item_ids)  # Use item_id instead of id
        items_dict = {str(item.item_id): item for item in items}  # Use item_id as the key

        for item_id, cart_item in self.cart.items():
            if item_id in items_dict:
                cart_item['item'] = items_dict[item_id]  # Correctly assign the Item object
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