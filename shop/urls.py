from django.urls import path
from .views import *
from .api import api_change_cart
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('api/change_cart', api_change_cart, name = "api_change_cart"),
    path('cart', cart, name = "cart"),
    path('checkout', checkout, name = "checkout"),
    path('registration', registration, name = "registration"),
    path('detail/<slug:product_slug>', detail, name = "detail"),
    path('logout_view', logout_view, name = "logout_view"),
    path('login_view', login_view, name = "login_view"),
    path('contact', contact, name = "contact"),
    path('my_orders', my_orders, name = "my_orders"),
    path('order_detail/<int:order_id>', order_detail, name = "order_detail"),
    path('', index, name = "index"),
    path('shop', shop, name = "shop")
]
