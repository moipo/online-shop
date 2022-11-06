from django.urls import path
from .views import *

urlpatterns = [
    path('', Shop.index),
    path('product/<slug:data>', Shop.product )
]
