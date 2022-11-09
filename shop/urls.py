from django.urls import path
from .views import *

urlpatterns = [
    path('', Shop.index),
    path('cart', Shop.cart, name = "cart"),
    path('product/<slug:product_slug>', Shop.product, name = "product" ),
    path('ProductApi/change_cart/', ProductApi.change_cart, name = "change_cart" ),
]
