from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .utils import get_cart


@api_view(["POST"])
def api_change_cart(request):
    product_id = request.data.get("product_id")
    action = request.data.get("action")

    crt = get_cart(request)
    order_items = crt.orderitem_set.all()

    order_item, _ = order_items.get_or_create(
        product=Product.objects.get(id=product_id),
        defaults={
            "order": crt,
            "product": Product.objects.get(pk=product_id),
            "quantity": 0,
        },
    )

    match action:
        case "add":
            order_item.quantity += 1
        case "remove":
            order_item.quantity -= 1

    order_item.save()

    order_item_quantity = order_item.quantity
    order_item_total_price = order_item.total_item_price

    if order_item.quantity <= 0:
        order_item.delete()

    total_quantity = sum(item.quantity for item in order_items)
    total_price = sum(item.total_item_price for item in order_items)
    return Response(
        {
            "total_quantity": total_quantity,
            "total_price": total_price,
            "order_item_quantity": order_item_quantity,
            "order_item_total_price": order_item_total_price,
        }
    )
