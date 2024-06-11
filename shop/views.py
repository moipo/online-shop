from collections.abc import Mapping
from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .models import *
from .utils import get_cart, merge_visitor_and_user_carts


def cart(request):
    crt = get_cart(request)
    order_items = crt.orderitem_set.all()
    ctx = {
        "order_items": order_items,
        "crt_total_quantity": crt.order_total_quantity,
        "crt_total_price": crt.total_order_price,
    }
    return render(request, "cart.html", ctx)


@login_required(login_url="/login_view")
def checkout(request):

    crt = Order.objects.get(customer=request.user, status="Cart")
    total_order_price = crt.total_order_price

    if request.method == "POST":
        shipping_address_form = ShippingAddressForm(request.POST)
        card_form = CardForm(request.POST)
        if shipping_address_form.is_valid() and card_form.is_valid():

            user = request.user
            order = get_object_or_404(Order, customer=user, status="Cart")

            shipping_address = shipping_address_form.save(commit=False)
            shipping_address.customer = user
            shipping_address.order = order
            shipping_address.save()

            order.status = "Pending"
            order.save()

            crt, _ = Order.objects.get_or_create(customer=user, status="Cart")
            return redirect("my_orders")

        messages.error(request, "All the fields must be filled")
        ctx = {
            "shipping_address_form": shipping_address_form,
            "card_form": card_form,
            "total_order_price": total_order_price,
        }
        return render(request, "checkout.html", ctx)

    shipping_address_form = ShippingAddressForm()
    card_form = CardForm()
    ctx = {
        "shipping_address_form": shipping_address_form,
        "total_order_price": total_order_price,
        "card_form": card_form,
    }
    return render(request, "checkout.html", ctx)


def detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    ctx = {"product": product}
    return render(request, "detail.html", ctx)


def index(request):
    return render(request, "index.html", {})


def shop(request):
    data = request.GET

    price_filter: str = data.get("price_filter", "price_all")
    search_string: str = data.get("search_string", "")
    page: int | None = data.get("page", 1)

    price_range_by_price_filter: Mapping[str, tuple(int | None, int | None)] = {
        "price_all": (None, None),
        "price_1_300": (1, 300),
        "price_300_1500": (300, 1500),
        "price_1500_5000": (1500, 5000),
        "price_5000": (5000, None),
    }
    start_price, end_price = price_range_by_price_filter[price_filter]

    filter_kwargs: dict = {}

    if start_price:
        filter_kwargs["price__gte"] = start_price
    if end_price:
        filter_kwargs["price__lte"] = end_price

    if search_string:
        filter_kwargs["name__icontains"] = search_string

    filtered_products = Product.objects.filter(**filter_kwargs)

    paginator = Paginator(filtered_products, 11)
    selected_products = paginator.page(page)

    ctx = {
           "selected_products": selected_products,
           "paginator": paginator,
           "page": page,
           "price_filter": price_filter,
           }

    if search_string:
        ctx["previous_search_string"] = search_string

    return render(request, "shop.html", ctx)


@login_required(login_url="/login_view")
def my_orders(request):
    orders_made = Order.objects.exclude(status="Cart").filter(customer=request.user)
    ctx = {
        "orders_made": orders_made,
    }
    return render(request, "orders/my_orders.html", ctx)


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    user = request.user
    if user == order.customer and user.is_authenticated:
        order_items = OrderItem.objects.all().filter(order=order)
        ctx = {
            "order": order,
            "order_items": order_items,
        }
        return render(request, "orders/order_detail.html", ctx)
    return HttpResponseForbidden()


def registration(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_is_new = not User.objects.filter(email=email).exists()
        if user_form.is_valid() and user_is_new:
            new_user = User.objects.create_user(
                username=email,
                email=email,
                first_name=request.POST.get("first_name"),
                password=password,
            )
            merge_visitor_and_user_carts(request=request, user=new_user)
            login(request, new_user)
            return redirect("shop")

        user_form = UserForm(request.POST)
        ctx = {
            "error": "Such email already exists",
            "user_form": user_form,
        }
        return render(request, "login/registration.html", ctx)

    user_form = UserForm()
    ctx = {
        "user_form": user_form,
    }
    return render(request, "login/registration.html", ctx)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            merge_visitor_and_user_carts(request=request, user=user)
            login(request, user)
            return redirect("cart")
        user_form = UserForm(request.POST)
        messages.error(request, "Wrong password or email")
        ctx = {
            "user_form": user_form,
        }
        return render(request, "login/login_view.html", ctx)

    user_form = UserForm()
    ctx = {
        "user_form": user_form,
    }
    return render(request, "login/login_view.html", ctx)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    crt, _ = Order.objects.get_or_create(customer=None, status="Cart")
    crt.delete()
    return redirect("shop")
