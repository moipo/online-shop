from django.urls import path

from .api import api_change_cart
from .views import (
    cart,
    checkout,
    detail,
    index,
    login_view,
    logout_view,
    my_orders,
    order_detail,
    registration,
    shop,
)

urlpatterns = [
    path("api/change_cart", api_change_cart, name="api_change_cart"),
    path("cart", cart, name="cart"),
    path("checkout", checkout, name="checkout"),
    path("registration", registration, name="registration"),
    path("detail/<slug:product_slug>", detail, name="detail"),
    path("logout_view", logout_view, name="logout_view"),
    path("login_view", login_view, name="login_view"),
    path("my_orders", my_orders, name="my_orders"),
    path("order_detail/<int:order_id>", order_detail, name="order_detail"),
    path("", index, name="index"),
    path("shop", shop, name="shop"),
]
