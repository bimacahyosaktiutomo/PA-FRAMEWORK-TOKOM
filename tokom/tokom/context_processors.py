from .cart import Cart

# def cart(request):
#     return {'cart': Cart(request)}

def cart(request):
    """Returns the cart to be used in templates."""
    cart = Cart(request)  # Cart is being stored in the session
    return {'cart': cart}
