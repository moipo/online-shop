from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.

class Shop:
    def index(request):
        products = Product.objects.all()
        ctx = {
        "products" : products,
        }
        return render(request, "check/index.html", ctx)


    def product(request, product_slug):
        ctx = {}
        return render(request, "check/product.html", ctx)


    def cart(request):
        ctx = {}
        return render(request, "check/cart.html", ctx)

    def registration(request):

        user_form = UserForm()

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username, password)
            if user is None:
                User.objects.create_user(username = username, password = password)
                return render(request, "", {})
            else:
                ctx = {
                "error" : "Такой пользователь уже существует. Попробуйте снова.",
                "user_form" : user_form
                }
                return render(request, "thesameview", ctx)
        ctx = {
        "user_form" : user_form
        }
        return render(request, "thesameview", ctx)



    def login_view(request):
        user_form = UserForm()
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request , username =  username, password = password)
            if user is not None:
                login(request,user)
                return redirect("login_view")
        ctx = {
        "user_form" : user_form,
        }
        return render(request, "login_view", ctx)

    def logout_view(request):
        if request.user.is_authenticated:
            logout(request)





class ProductApi:
    def add_to_cart(request,*args,**kwargs):
        quantity = request.GET.get("quantity")
        print(quantity)
        data_from_server = "SUCCESS!"
        return JsonResponse(
        {
        "data_from_server" : data_from_server,
        }
        )











    #def registration
    # def create_order(request):
    #     OrderFormSet = inlineformset_factory(Product, Order)
    #
