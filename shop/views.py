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
        if request.user.is_authenticated:
            user = request.user
        crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        order_items = crt.orderitem_set.all()


        ctx = {
        "products" : products,
        "crt_total_quantity" : crt.order_total_quantity,
        }
        return render(request, "check/index.html", ctx)


    def product(request, product_slug):
        ctx = {}
        return render(request, "check/product.html", ctx)



    def cart(request): # view with all the OrderItems

        if request.user.is_authenticated:
            user = request.user
            crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
            order_items = crt.orderitem_set.all()
        else:
            order_items = []


        ctx = {
        "order_items" : order_items,
        "crt_total_quantity": crt.order_total_quantity,
        "crt_total_price": crt.order_total_price,
        }
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





# class ProductApi:
#     def change_cart(request):
#         product_id = request.GET.get("product_id")
#         action = request.GET.get("action")
#         print(product_id, action)
#         user = request.user
#         if request.user.is_authenticated:
#             crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
#             order_items = crt.orderitem_set.all()
#             order_item , created = order_items.get_or_create(
#                 product = Product.objects.get(id = product_id),
#                 defaults = {
#                     "order":crt,
#                     "product":Product.objects.filter(id = product_id)[0] ,
#                     "quantity" : 0
#                     }
#                 )
#             order_item.quantity += 1
#             order_item.save()
#
#
#             total_quantity = sum([item.quantity for item in order_items])
#
#             return JsonResponse(
#             {
#             "total_quantity" : total_quantity,
#             }
#             )
