from itertools import product

from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products , "quantities":quantities, "totals": totals},  )


def cart_add(request):
    ## get the cart
    cart = Cart(request)
    # test the post
    if request.POST.get('action') == 'post':
        # get some stuff
        product_id = int(request.POST.get('product_id'))
        # grab also the quantity
        product_qty = int(request.POST.get('product_qty'))
        # lookup product in the db
        product = get_object_or_404(Product, pk=product_id)
        # save it to the session
        cart.add(product=product, quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()
        # return the response
        response = JsonResponse({'Product Name': product.name})
        messages.success(request, 'Product Added to cart!!!')
        return JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # Create a Cart instance and call its delete method
        cart = Cart(request)
        cart.delete(product_id)
        messages.success(request, 'Product Deleted from cart!!!')
        return JsonResponse({'product': product_id})



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, 'Product quantity Updated successfully!')
        response = JsonResponse({'qty': product_qty})
        return response
        #return redirect('cart_summary')