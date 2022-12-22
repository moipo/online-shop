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
    path('cart', Shop.cart, name = "cart"),
    path('checkout', Shop.checkout, name = "checkout"),
    path('registration', Who.registration, name = "registration"),
    path('detail/<slug:product_slug>', Shop.detail, name = "detail"),
    path('logout_view', Who.logout_view, name = "logout_view"),
    path('login_view', Who.login_view, name = "login_view"),
    path('contact', Shop.contact, name = "contact"),
    path('my_orders', Shop.my_orders, name = "my_orders"),
    path('order_detail/<int:order_id>', Shop.order_detail, name = "order_detail"),
    path('', Shop.index, name = "index"),
    path('shop', Shop.populate_db, name = "shop")
]
