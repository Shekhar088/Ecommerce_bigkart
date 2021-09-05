from carts.models import Cart, CartItem
from accounts.forms import RegisterForm
from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart,CartItem

import requests 

# Create your views here.

def register(request):

    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
    
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name,
                password=password, email=email, username=username)
            user.phone_number= phone_number
            user.save()
            messages.success(request,"Registration successful")
            return redirect('login')

    else:
        form = RegisterForm()

    context={
        'form':form,
    }
    return render(request,"accounts/register.html", context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user= auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart) 
                    
                    for item in cart_item:
                        item.user= user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')
        else:
            messages.ERROR(request,"Invalid credentials")
            return redirect("login")

    return render(request, "accounts/login.html")

@login_required(login_url = "login")
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect("login")

@login_required(login_url= 'login')
def dashboard(request):
    return render(request,"accounts/dashboard.html");