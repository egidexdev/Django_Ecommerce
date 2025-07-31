from django.shortcuts import render, redirect
from pyexpat.errors import messages

from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product , Profile


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get order
        order = Order.objects.get(id=pk)
        #get order items
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'payment/orders.html',{"order":order,"items":items})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_shipped=False)
        return render(request, 'payment/not_shipped_dash.html',
                  {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_shipped=True)
        return render(request, 'payment/shipped_dash.html',
                      {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')



def process_order(request):
    if request.method == 'POST':
        #the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        #getting the billing info
        payment_form = PaymentForm(request.POST or None)
        #get shipping info session data
        my_shipping = request.session.get('my_shipping')

        # let gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        #create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        #creat an order

        if request.user.is_authenticated:
            user = request.user
            #create an order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #add order items
            #the order id
            order_id = create_order.pk

            #get thr product info
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    # get qantity
                    for key, value in quantities().items():
                        if int(key) == product_id:
                            # create order item
                            create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                            create_order_item.save()

                            # delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            #delete also the model from db
            current_user = Profile.objects.filter(user__id=request.user.id)
            #delet shopping cart from db
            current_user.update(old_cart="")






            messages.success(request, 'Your order has been created.')
            return redirect('home')
        else:
            # not logged
            # create order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk

            # get thr product info
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    # get qantity
                    for key, value in quantities().items():
                        if int(key) == product_id:
                            # create order item
                            create_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                          quantity=value, price=price)
                            create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]


            messages.success(request, 'Your order has been created.')
            return redirect('home')
    else:
        messages.success(request , "Access denied")
        return redirect("home")


def billing_info(request):
    if request.method == 'POST':
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        #create session with shippping  info
        my_shippping = request.POST
        request.session['my_shipping'] = my_shippping

        #check to see if user is logged in
        if request.user.is_authenticated:
            #get the billing info
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST, "billing_form":billing_form})
        else:
            # not logged
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST, "billing_form": billing_form})


        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/billing_info.html',
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form}, )
    else:
        messages.success(request , "Access denied")
        return redirect("home")


def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Safe way to fetch shipping address
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()

        if shipping_user:
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        else:
            shipping_form = ShippingForm(request.POST or None)

        return render(request, 'payment/checkout.html',
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form})

    else:
        # checking out as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html',{})

