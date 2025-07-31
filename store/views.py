from django.db.models.expressions import result
from django.shortcuts import render, redirect
from unicodedata import category
import json

from .models import Product , Category, Profile
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm, UpdateUserForm , UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
from  cart.cart import Cart


def search(request):
    #if they filled the form
    if request.method == "POST":
        searched = request.POST.get('searched')
        #queerry the peoducts from databse model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
            messages.success(request, 'Sorry Could not find that product')
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        # Get current user profile
        current_user = Profile.objects.get(user=request.user)

        # Try to get shipping address, or set to None if not found
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()

        # Initialize forms with POST data or instance
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == "POST":
            if form.is_valid() and shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, 'Your info has been updated successfully ✅')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')

        return render(request, 'update_info.html', {
            'form': form,
            'shipping_form': shipping_form
        })

    else:
        messages.error(request, 'You must be logged in to access this page ❌')
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User has been Updated successfully!!')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'You must be logged in to access this page !!')
        return redirect('home')



def category(request, foo):
    #for replacing the hyphen tag in the url  with the space
    foo = foo.replace('-', ' ')
    #grab category from url
    try:
        #look for category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("that Category doesn't exist"))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {"product": product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # let do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #let get their saved cart from DB
            saved_cart = current_user.old_cart
            #convert db string to python dictionary
            if saved_cart:
                # convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                # add the loaded dictionary to the session
                #get the cart
                cart = Cart(request)
                #loop through the and add the items from DB
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #lets login user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully!!!')
            return redirect('update_info')
        else:
            messages.success(request, 'There was a problem in registering please try again later')
            return redirect('register')
    else:
            return render(request, 'register.html', {'form': form})



