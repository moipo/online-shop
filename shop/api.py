from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import OrderItem, Product
from .utils import get_cart


@api_view(["POST"])
def api_change_cart(request):
    product_id = request.data.get("product_id")
    action = request.data.get("action")

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return Response({"detail": "product_id must be an integer."}, status=400)

    if action not in {"add", "remove"}:
        return Response(
            {"detail": "action must be either 'add' or 'remove'."}, status=400
        )

    product = get_object_or_404(Product, pk=product_id)

    with transaction.atomic():
        cart_order = get_cart(request)
        order_item, _ = OrderItem.objects.select_for_update().get_or_create(
            order=cart_order,
            product=product,
            defaults={"quantity": 0},
        )

        quantity_delta = 1 if action == "add" else -1
        order_item.quantity = (order_item.quantity or 0) + quantity_delta

        if order_item.quantity <= 0:
            order_item.delete()
            order_item_quantity = 0
            order_item_total_price = 0
        else:
            order_item.save(update_fields=["quantity"])
            order_item_quantity = order_item.quantity
            order_item_total_price = order_item.total_item_price

        order_items = cart_order.orderitem_set.select_related("product").all()
        total_quantity = sum(item.quantity or 0 for item in order_items)
        total_price = sum(item.total_item_price for item in order_items)
    return Response(
        {
            "total_quantity": total_quantity,
            "total_price": total_price,
            "order_item_quantity": order_item_quantity,
            "order_item_total_price": order_item_total_price,
        }
    )
