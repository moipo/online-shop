from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

@api_view(["GET", "POST"])
def api_change_cart(request):
    product_id = request.data.get("product_id")
    action = request.data.get("action")

    user = request.user

    if request.user.is_authenticated:
        crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
    else:
        crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
    order_items = crt.orderitem_set.all()


    order_item , created = order_items.get_or_create(
        product = Product.objects.get(id = product_id),
        defaults = {
            "order":crt,
            "product":Product.objects.filter(id = product_id)[0] ,
            "quantity" : 0
            }
        )
    if action == "add":
        order_item.quantity += 1
    if action == "remove":
        order_item.quantity -= 1
    order_item.save()

    order_item_quantity = order_item.quantity
    order_item_total_price = order_item.total_item_price


    if order_item.quantity <= 0: order_item.delete()


    total_quantity = sum([item.quantity for item in order_items])
    total_price = sum([item.total_item_price for item in order_items])


    return Response(
        {
        "total_quantity" : total_quantity,
        "total_price":total_price,


        "order_item_quantity" : order_item_quantity,
        "order_item_total_price": order_item_total_price,

        }
    )
