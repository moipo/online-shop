from .models import Order

def get_cart(request):
    user = request.user
    if user.is_authenticated:
        crt, created = Order.objects.get_or_create(customer = user, status = "Cart")
    else:
        crt, created = Order.objects.get_or_create(customer = None, status = "Cart")
    return crt
