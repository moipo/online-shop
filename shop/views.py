from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages



# Create your views here.

class Prototype:
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










class Shop:

    @staticmethod
    def get_cart_total(request):
        user = request.user
        if request.user.is_authenticated:
            crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        else:
            crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
        return crt.order_total_quantity

    def cart(request):

        user = request.user

        if request.user.is_authenticated:
            crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        else:
            crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
        order_items = crt.orderitem_set.all()


        ctx = {
        "order_items" : order_items,
        "crt_total_quantity": crt.order_total_quantity,
        "crt_total_price": crt.order_total_price,
        }

        return render(request,"cart.html",ctx)

    @login_required(login_url = "/registration")
    def checkout(request):


        # if request.method == "POST":
        #     form = ShippingAddressForm(request.POST)
        #     if form.is_valid():
        #         pass
        #     else:


        shipping_address_form = ShippingAddressForm()
        ctx = {
        "shipping_address_form":shipping_address_form,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request,"checkout.html",ctx)


    def contact(request):
        ctx = {
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request,"contact.html",ctx)

    def detail(request, product_slug):
        product = Product.objects.get(slug = product_slug)
        ctx = {
        "product":product,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request,"detail.html",ctx)

    def index(request):
        ctx = {
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request,"index.html",ctx)

    def shop(request):

        user = request.user

        if request.user.is_authenticated:
            crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        else:
            crt, created = Order.objects.get_or_create(customer = None, status = "Cart")


        all_products = Product.objects.all()
        ctx = {
        "all_products" : all_products,
        "crt_total_quantity": crt.order_total_quantity,
        }
        return render(request,"shop.html",ctx)




class Who:
    def registration(request):



        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username = email, password = password)
            if user is None:
                new_user = User.objects.create_user(username = email, email = email, first_name = request.POST.get("first_name"), password = password)
                new_user.save()
                login(request,new_user)

                crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
                crt.customer = new_user
                crt.save()

                crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
                crt.delete()

                return redirect("shop")
            else:
                user_form = UserForm(request.POST)
                ctx = {
                "error" : "‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎Such email already exists",
                "user_form" : user_form,
                "crt_total_quantity": Shop.get_cart_total(request),
                }
                return render(request, "who/registration.html", ctx)

        user_form = UserForm()
        ctx = {
        "user_form" : user_form,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request, "who/registration.html", ctx)



    def login_view(request):

        if request.method == "POST":

            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request , username =  email, password = password)
            if user is not None:
                login(request,user)
                return redirect("cart")
            else:
                user_form = UserForm(request.POST)
                messages.error(request, "Wrong password or username")
                ctx = {
                "crt_total_quantity": Shop.get_cart_total(request),
                "user_form" : user_form,
                }
                return render(request, "who/login_view.html",ctx)

        user_form = UserForm()
        ctx = {
        "user_form" : user_form,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request, "who/login_view.html", ctx)



    def logout_view(request):
        if request.user.is_authenticated:
            logout(request)

        crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
        crt.delete()

        return redirect("shop")

# class ProductApi:
#     def change_cart(request):
#         print(request.POST.get("foo"))
#         product_id = request.body[1]
#         action = request.body[3]
#         print("method is being executed")
#         print(product_id, action)
#
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
