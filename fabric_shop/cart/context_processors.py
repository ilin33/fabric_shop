from .cart import Cart

def cart_quantity(request):
    cart = Cart(request)
    return {'cart_total_items': len(cart)}
