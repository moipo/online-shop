from django.urls import path
from .views import *
from .api import api_change_cart

urlpatterns = [
    path('prototype', Prototype.index),
    path('prototype/cart', Prototype.cart, name = "prototype_cart"),
    path('prototype/product/<slug:product_slug>', Prototype.product, name = "prototype_product" ),
    # path('prototype/ProductApi/change_cart', ProductApi.change_cart, name = "change_cart" ),

    path('api/change_cart', api_change_cart, name = "api_change_cart"),
    path('cart', Shop.cart, name = "cart"),
    path('checkout', Shop.checkout, name = "checkout"),
    path('contact', Shop.contact, name = "contact"),
    path('detail', Shop.detail, name = "detail"),
    path('index', Shop.index, name = "index"),
    path('shop', Shop.shop, name = "shop")

]
