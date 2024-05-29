from .utils import get_cart


def get_cart_total(request):
    crt = get_cart(request)
    return {"crt_total_quantity": crt.order_total_quantity}
