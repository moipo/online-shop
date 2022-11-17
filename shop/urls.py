from django.urls import path
from .views import *
from .api import api_change_cart

urlpatterns = [
    path('', Prototype.index),
    path('cart', Prototype.cart, name = "cart"),
    path('product/<slug:product_slug>', Prototype.product, name = "product" ),
    # path('ProductApi/change_cart', ProductApi.change_cart, name = "change_cart" ),
    path('api/change_cart', api_change_cart, name = "api_change_cart"),
    path('shop/index', Shop.index, name = "shop_index")
]
