from cart.cart import Cart  # or your custom session cart class

def cart_count(request):
    cart = Cart(request)
    return {'cart_count': cart.count()}
