from email.policy import default

from .cart import Cart

def cart(request):
    #return default data from the cart
    return {'cart': Cart(request)}