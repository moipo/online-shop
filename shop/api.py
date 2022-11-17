from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


@api_view(["GET", "POST"])
def api_change_cart(request):
    product_id = request.GET.get("product_id")
    action = request.GET.get("action")
    print(product_id, action)
    user = request.user
    if request.user.is_authenticated:
        crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
        order_items = crt.orderitem_set.all()
        order_item , created = order_items.get_or_create(
            product = Product.objects.get(id = product_id),
            defaults = {
                "order":crt,
                "product":Product.objects.filter(id = product_id)[0] ,
                "quantity" : 0
                }
            )
        order_item.quantity += 1
        order_item.save()


        total_quantity = sum([item.quantity for item in order_items])

        return Response(
            {
            "total_quantity" : total_quantity,
            }
        )
