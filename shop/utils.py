from .models import Order


def get_cart(request):
    user = request.user
    if user.is_authenticated:
        crt, _ = Order.objects.get_or_create(customer=user, status="Cart")
    else:
        crt, _ = Order.objects.get_or_create(customer=None, status="Cart")
    return crt
