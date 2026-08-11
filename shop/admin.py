from django.contrib import admin

from .models import Order, OrderItem, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "added_at")


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "date_added")


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "date_added")


admin.site.register(OrderItem, OrderItemAdmin)
