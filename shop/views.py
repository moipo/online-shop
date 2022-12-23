from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime , timezone
from random import randint
from django.core.paginator import Paginator






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

    @login_required(login_url = "/login_view")
    def checkout(request):

        crt = Order.objects.get(customer = request.user, status = "Cart")
        order_total_price = crt.order_total_price

        if request.method == "POST":


            shipping_address_form = ShippingAddressForm(request.POST)
            card_form = CardForm(request.POST)
            if shipping_address_form.is_valid() and card_form.is_valid ():
                print("forms_are_valid")
                ship_addr = shipping_address_form.save()
                card = card_form.save()

                user = request.user
                ship_addr.customer = user
                card.customer.set(User.objects.filter(id = user.id))
                order = get_object_or_404(Order, customer = user, status = "Cart")
                order.status = "Pending"
                order.save()
                ship_addr.order = order
                card.order = order
                card.save()

                ship_addr.save()

                crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
                crt.save()

                ctx = {
                "crt_total_quantity": Shop.get_cart_total(request),
                }

                return redirect("my_orders")
            else:

                messages.error(request,"All the fields must be filled")
                ctx = {
                "shipping_address_form": shipping_address_form,
                "crt_total_quantity": Shop.get_cart_total(request),
                "card_form" : card_form ,
                "order_total_price" : order_total_price,
                }
                return render(request,"checkout.html",ctx)



        shipping_address_form = ShippingAddressForm()
        card_form = CardForm()
        ctx = {
        "shipping_address_form":shipping_address_form,
        "crt_total_quantity": Shop.get_cart_total(request),
        "order_total_price" : order_total_price,
        "card_form": card_form,
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
        crt_total_quantity = Shop.get_cart_total(request)
        user = request.user
        if not user.is_authenticated and crt_total_quantity!=0:

            now = datetime.now(timezone.utc)

            crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
            order_items = crt.orderitem_set.all()
            last_change = max([i.date_added for i in order_items])


            diff = now-last_change
            num = round(int(float(str(diff.total_seconds() * 1000)))/1000,0)
            no_changes = int(num)
            print(no_changes)
            if no_changes > 900:
                map(lambda x : x.delete(), order_items)
                [i.delete() for i in order_items]

        crt_total_quantity = Shop.get_cart_total(request)




        ctx = {

        "crt_total_quantity": crt_total_quantity,
        }
        return render(request,"index.html",ctx)

    # def shop(request):
    #
    #     # print(request.GET)
    #     # print("data")
    #
    #     user = request.user
    #
    #     if request.user.is_authenticated:
    #         crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
    #     else:
    #         crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
    #
    #
    #
    #     data = request.GET
    #
    #     last_checkbox_name = "price-0"
    #     if data:
    #
    #         rng = ""
    #
    #         for i in range(0,5):
    #             try:
    #                 rng = data[f"price-{i}"]
    #                 last_checkbox_name = f"price-{i}"
    #             except:
    #                 continue
    #         start, end = map(lambda x: int(x), rng.split())
    #
    #         all_products = Product.objects.all()
    #         selected_products = all_products.filter(price__gte = start, price__lte = end)
    #     else:
    #         selected_products = Product.objects.all()
    #
    #
    #
    #     ctx = {
    #     "last_checkbox_name" : last_checkbox_name,
    #     "selected_products" : selected_products,
    #     "crt_total_quantity": crt.order_total_quantity,
    #     }
    #     return render(request,"shop.html",ctx)

    def shop(request):

        print(request.GET)
        # print("data")

        user = request.user

        if request.user.is_authenticated:
            crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        else:
            crt, created = Order.objects.get_or_create(customer = None, status = "Cart")



        data = request.GET

        last_checkbox_name = "price-0"
        try:
            if data:

                rng = ""

                for i in range(0,5):
                    try:
                        rng = data[f"price-{i}"]
                        last_checkbox_name = f"price-{i}"
                    except:
                        continue
                start, end = map(lambda x: int(x), rng.split())

                selected_products = Product.objects.all().filter(price__gte = start, price__lte = end)
            else:
                selected_products = Product.objects.all()
        except:
            selected_products = Product.objects.all()



        if "search_string" in request.GET and request.GET['search_string']:
            page = request.GET.get('page', 1)

            search_string = request.GET['search_string']
            products = Product.objects.filter(name__icontains = search_string).order_by('name')
            paginator = Paginator(products, 11)
            selected_products = paginator.page(page)


            ctx = {

            "last_checkbox_name" : last_checkbox_name,
            "selected_products" : selected_products,
            "crt_total_quantity": crt.order_total_quantity,
            "paginator":paginator,
            "previous_search_string":search_string,
            }

        else:

            page = request.GET.get('page', 1)
            paginator = Paginator(selected_products, 11)
            selected_products = paginator.page(page)

            ctx = {
            "last_checkbox_name" : last_checkbox_name,
            "selected_products" : selected_products,
            "crt_total_quantity": crt.order_total_quantity,
            "paginator":paginator,
            }


        return render(request,"shop.html",ctx)




    @login_required(login_url = "/login_view")
    def my_orders(request):
        orders_made = Order.objects.exclude(status = "Cart").filter(customer = request.user)
        ctx = {
        "orders_made" : orders_made,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request,"orders/my_orders.html",ctx)

    def order_detail(request, order_id):
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.all().filter(order = order)
        ctx = {
        "order":order,
        "order_items" : order_items,
        "crt_total_quantity": Shop.get_cart_total(request),
        }
        return render(request, "orders/order_detail.html", ctx)

    # def populate_db(request):
    #     prdcts = Product.objects.all()
    #     template_letters = "XZYMNDSWBLGQ"
    #     for _ in range(7):
    #         for pr in prdcts:
    #             letter_1 = template_letters[randint(10, 100)%len(template_letters)]
    #             letter_2 = template_letters[randint(10, 100)%len(template_letters)]
    #             number = str(randint(10, 100))
    #             Product.objects.get_or_create(
    #                 name = letter_1+letter_2+"-"+number,
    #                 price = pr.price + randint(99, 7641),
    #                 description = pr.description ,
    #                 rating = pr.rating ,
    #                 pic = pr.pic ,
    #                 added_at = pr.added_at ,
    #                 category = pr.category ,
    #                 slug = pr.slug ,
    #             )
    #     return render(request, "shop.html", {})

# def search(request, page_num=1, search_string_pag = None):
#         if search_string_pag == "None":
#             search_string_pag = None
#
#         search_string= request.GET.get('search_string')
#
#         if search_string is not None:
#             page_num = 1
#
#         if search_string_pag is not None:
#             search_string = search_string_pag
#
#         res = ""
#         if search_string is not None:
#             res = Product.objects.filter(
#                 Q(name__icontains=search_string) | Q(model__icontains=search_string)
#             )
#
#         else:
#             res = Product.objects.all()
#
#
#         search_string= request.GET.get('search_string')
#         try:
#             if search_string_pag != search_string:
#                 res = Product.objects.filter(name__icontains=search_string)
#                 )
#         except: pass
#         p = Paginator(res,10)
#         page_obj = p.get_page(page_num)
#
#         if request.GET.get('search_string') is None:
#             search_string = search_string_pag
#
#         ctx = {
#         "page_obj":page_obj,
#         "search_string":search_string,
#         }
#         return render(request, "general/search.html",ctx)




class Who:
    def registration(request):

        if request.method == "POST":
            user_form = UserForm(request.POST)
            email = request.POST.get("email")
            password = request.POST.get("password")
            email_doesnt_exist = email not in [u.email for u in User.objects.all()]
            if user_form.is_valid() and email_doesnt_exist:
                new_user = User.objects.create_user(username = email, email = email, first_name = request.POST.get("first_name"), password = password)
                new_user.save()
                login(request,new_user)

                crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
                crt.customer = new_user
                crt.save()

                crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
                crt.delete()

                return redirect("shop")


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
                messages.error(request, "Wrong password or email")
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
