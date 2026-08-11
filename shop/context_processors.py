from .utils import get_cart


def get_cart_total(request):
    cart = get_cart(request, create=False)
    return {"crt_total_quantity": cart.order_total_quantity if cart else 0}
