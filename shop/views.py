from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CardForm, ShippingAddressForm, UserForm
from .models import Order, OrderItem, Product
from .utils import get_cart, merge_visitor_and_user_carts


PRICE_RANGES = {
    "price_all": (None, None),
    "price_1_300": (1, 300),
    "price_300_1500": (300, 1500),
    "price_1500_5000": (1500, 5000),
    "price_5000": (5000, None),
}


def cart(request):
    cart_order = get_cart(request)
    order_items = cart_order.orderitem_set.select_related("product").all()
    ctx = {
        "order_items": order_items,
        "crt_total_quantity": cart_order.order_total_quantity,
        "crt_total_price": cart_order.total_order_price,
    }
    return render(request, "cart.html", ctx)


@login_required(login_url="/login_view")
def checkout(request):
    cart_order = get_cart(request)
    if not cart_order.orderitem_set.exists():
        messages.info(request, "Your cart is empty.")
        return redirect("cart")

    shipping_address_form = ShippingAddressForm(request.POST or None)
    card_form = CardForm(request.POST or None)
    if request.method == "POST":
        if shipping_address_form.is_valid() and card_form.is_valid():
            with transaction.atomic():
                order = get_object_or_404(
                    Order.objects.select_for_update(),
                    pk=cart_order.pk,
                    customer=request.user,
                    status="Cart",
                )
                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.customer = request.user
                shipping_address.order = order
                shipping_address.save()

                order.status = "Pending"
                order.save(update_fields=["status"])
            return redirect("my_orders")

        messages.error(request, "All the fields must be filled")
    ctx = {
        "shipping_address_form": shipping_address_form,
        "card_form": card_form,
        "total_order_price": cart_order.total_order_price,
    }
    return render(request, "checkout.html", ctx)


def detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    ctx = {"product": product}
    return render(request, "detail.html", ctx)


def index(request):
    return render(request, "index.html")


def shop(request):
    price_filter = request.GET.get("price_filter", "price_all")
    if price_filter not in PRICE_RANGES:
        price_filter = "price_all"
    start_price, end_price = PRICE_RANGES[price_filter]

    search_string = request.GET.get("search_string", "").strip()
    page = request.GET.get("page", 1)
    filter_kwargs = {}

    if start_price is not None:
        filter_kwargs["price__gte"] = start_price
    if end_price is not None:
        filter_kwargs["price__lte"] = end_price

    if search_string:
        filter_kwargs["name__icontains"] = search_string

    filtered_products = Product.objects.filter(**filter_kwargs).order_by("pk")

    paginator = Paginator(filtered_products, 11)
    selected_products = paginator.get_page(page)

    ctx = {
        "selected_products": selected_products,
        "paginator": paginator,
        "page": selected_products.number,
        "price_filter": price_filter,
    }

    if search_string:
        ctx["previous_search_string"] = search_string

    return render(request, "shop.html", ctx)


@login_required(login_url="/login_view")
def my_orders(request):
    orders_made = (
        Order.objects.exclude(status="Cart")
        .filter(customer=request.user)
        .prefetch_related("orderitem_set__product")
        .order_by("-date_added")
    )
    ctx = {
        "orders_made": orders_made,
    }
    return render(request, "orders/my_orders.html", ctx)


@login_required(login_url="/login_view")
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    order_items = OrderItem.objects.filter(order=order).select_related("product")
    ctx = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, "orders/order_detail.html", ctx)


def registration(request):
    user_form = UserForm(request.POST or None)
    if request.method == "POST":
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            new_user = User.objects.create_user(
                username=form_data["email"],
                email=form_data["email"],
                first_name=form_data["first_name"],
                password=form_data["password"],
            )
            merge_visitor_and_user_carts(request=request, user=new_user)
            login(request, new_user)
            return redirect("shop")

        ctx = {
            "error": "Please correct the errors below.",
            "user_form": user_form,
        }
        return render(request, "login/registration.html", ctx)

    ctx = {
        "user_form": user_form,
    }
    return render(request, "login/registration.html", ctx)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
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


@login_required(login_url="/login_view")
def logout_view(request):
    logout(request)
    return redirect("shop")
