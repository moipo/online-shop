from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Product._meta.fields]
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Order._meta.fields]
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = [x.name for x in OrderItem._meta.fields]
admin.site.register(OrderItem, OrderItemAdmin)

class WebsocketInfoAdmin(admin.ModelAdmin):
    list_display = [x.name for x in WebsocketInfo._meta.fields]
admin.site.register(WebsocketInfo, WebsocketInfoAdmin)
