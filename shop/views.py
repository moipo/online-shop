from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .enums import PriceFilters
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
    crt_total_quantity = get_cart(request).order_total_quantity
    user = request.user
    if not user.is_authenticated and crt_total_quantity != 0:

        crt, _ = Order.objects.get_or_create(customer=None, status="Cart")
        order_items = crt.orderitem_set.all()
        last_change = max(i.date_added for i in order_items)

        now = datetime.now(timezone.utc)
        diff = now - last_change
        num = round(int(float(str(diff.total_seconds() * 1000))) / 1000, 0)
        no_changes = int(num)

        if no_changes > 900:
            map(lambda x: x.delete(), order_items)
            [i.delete() for i in order_items]

    return render(request, "index.html", {})


# def shop(request):
#     request.GET[PriceFilters.PRICE1.value]

def shop(request):
    data = request.GET

    last_checkbox_name = "price-0"
    last_checkbox_range = ""
    try:
        if data:
            for i in range(0, 5):
                try:
                    last_checkbox_range = data[f"price-{i}"]
                    last_checkbox_name = f"price-{i}"
                except:
                    continue
            start, end = map(lambda x: int(x), last_checkbox_range.split())
            selected_products = Product.objects.all().filter(
                price__gte=start, price__lte=end
            )
        else:
            selected_products = Product.objects.all()
    except:
        selected_products = Product.objects.all()

    last_checkbox_range = "+".join(last_checkbox_range.split())

    ctx = {
        "last_checkbox_name": last_checkbox_name,
        "last_checkbox_range": last_checkbox_range,
    }

    if "search_string" in request.GET and request.GET["search_string"]:
        page = request.GET.get("page", 1)

        search_string = request.GET["search_string"]
        products = selected_products.filter(name__icontains=search_string).order_by(
            "name"
        )
        paginator = Paginator(products, 11)
        selected_products = paginator.page(page)

        ctx["selected_products"] = selected_products
        ctx["paginator"] = paginator
        ctx["page"] = page
        ctx["previous_search_string"] = search_string

    else:
        page = request.GET.get("page", 1)
        paginator = Paginator(selected_products, 11)
        selected_products = paginator.page(page)

        ctx["selected_products"] = selected_products
        ctx["paginator"] = paginator
        ctx["page"] = page

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
    if user == order.customer and user.is_authenticated():
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
            merge_visitor_and_user_carts(request=request,user=new_user)
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
