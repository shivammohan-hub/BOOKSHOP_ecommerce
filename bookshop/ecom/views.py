from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from ecom.forms import AddressCheckoutForm


# Create your views here.
def homepage(req):
    data = {
        "genre" : Genre.objects.all(),
        "books" : Book.objects.all()
    }
    return render(req,"home.html",data)

def search(req):
    if req.GET.get("search"):
        search = req.GET.get("search")

        data = {
            "genres" : Genre.objects.all(),
            "books" : Book.objects.filter(title__icontains=search),
            "search":  search
        }
        return render(req, "filter.html",data)
    

def filterBygenre(req, genre_id):
    if genre_id:
        data = {
            "genres" : Genre.objects.all(),
            "books" : Book.objects.filter(genre_id=genre_id),
            "search":  Genre.objects.get(id=genre_id)
        }
        return render(req, "filter.html",data)
    

def bookDetails(req, book_id):
    if book_id:
        data = {
            "genres" : Genre.objects.all(),
            "book" : Book.objects.get(id=book_id),
            "related_books" : Book.objects.exclude(id=book_id)
        }
        return render(req, "book_details.html",data)
    

def login(req):
    form = AuthenticationForm(req.POST or None)
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(req, user)
            return redirect("homepage")
        else :
            print("Invalid credentials")
    data = {
        "loginForm" : form
    }
    return render(req, "login.html",data)


def register(req):
    form = UserCreationForm(req.POST or None) 
    if req.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.first_name = req.POST.get("fname")
            data.last_name = req.POST.get("lname")
            data.email = req.POST.get("email")
            data.save()
            return redirect("login")
    data = {
        "registerForm" : form
    }
    return render(req, "register.html",data)


def logout(req):
    auth_logout(req)
    return redirect("homepage")



def addToCart(req, book_id):
    try:
        book = Book.objects.get(id=book_id)
        order = Order.objects.filter(user_id=req.user, is_ordered=False).first()
        if order:
            order_item = OrderItem.objects.filter(user_id=req.user, book_id=book, order_id=order).first()
            if order_item:
                order_item.qty += 1
                order_item.save()
            else:
                order_item = OrderItem()
                order_item.user_id = req.user
                order_item.book_id = book
                order_item.order_id = order
                order_item.save()
        else:
            order = Order()
            order.user_id = req.user
            order.save()
            
            order_item = OrderItem()
            order_item.user_id = req.user
            order_item.book_id = book
            order_item.order_id = order
            order_item.save()
        return redirect("cart") 
        
    except Book.DoesNotExist:
        return redirect("cart") 


def cart(req):
    order = Order.objects.filter(user_id=req.user, is_ordered=False).first()
    order_items = OrderItem.objects.filter(order_id=order) if order else []

    data = {
        "order": order,
        "order_items": order_items,
    }
    return render(req, "cart.html", data)



def removeFromCart(req, book_id):
    try:
        book = Book.objects.get(id=book_id)
        order = Order.objects.filter(user_id=req.user, is_ordered=False).first()
        
        if order:
            order_item = OrderItem.objects.filter(user_id=req.user, book_id=book, order_id=order).first()
            if order_item:
                if order_item.qty > 1:
                    order_item.qty -= 1
                    order_item.save()
                else:
                    order_item.delete()
        return redirect("cart")  
        
    except Book.DoesNotExist:
        return redirect("cart")  


def applyCoupon(req):
    if req.method == "POST":
        code = req.POST.get("code")

        try:
            checkCoupon = Coupon.objects.get(code=code)

            order = Order.objects.filter(user = req.user, is_ordered = False).first()
            order.coupon_id = checkCoupon
            order.save()
            return redirect(cart)
        
        except Coupon.DoesNotExist:
            return redirect(cart)
        
    
def checkout(req):
    form = AddressCheckoutForm(req.POST or None)
    order = Order.objects.filter(user_id=req.user, is_ordered=False).first()
    addresses = Address.objects.filter(user_id=req.user)
    
    
    if req.POST.get("address_id"):
        try:
            address = Address.objects.get(id=req.POST.get("address_id"))
        except Address.DoesNotExist:
            print("not found saved address")
        order.address_id = address
        order.save()
        return redirect(checkout)
    else:
        if req.method == "POST":
            if form.is_valid():
                data = form.save(commit=False)
                data.user_id = req.user
                data.save()
                
                # update address id in order 
                order.address_id = data
                order.save()
                return redirect(checkout)

    return render(req, "checkout.html", {"form":form,"order":order,"addresses":addresses})