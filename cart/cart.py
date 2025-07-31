import json
from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get current session cart if it exists, else initialize it
        cart = self.session.get('session_key')
        if cart is None:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        # Save to user profile if logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            if current_user.exists():
                cart_json = json.dumps(self.cart)
                current_user.update(old_cart=cart_json)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        # Save to user profile if logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            if current_user.exists():
                cart_json = json.dumps(self.cart)
                current_user.update(old_cart=cart_json)

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get products based on IDs in the cart
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        return self.cart

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        self.cart[product_id] = product_qty
        self.session.modified = True

        # Save to user profile if logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            if current_user.exists():
                cart_json = json.dumps(self.cart)
                current_user.update(old_cart=cart_json)
        return self.cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        # Save to user profile if logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            if current_user.exists():
                cart_json = json.dumps(self.cart)
                current_user.update(old_cart=cart_json)

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            key = int(key)
            quantity = int(value)
            for product in products:
                if product.id == key:
                    price = product.sale_price if product.is_sale else product.price
                    total += price * quantity

        return total
