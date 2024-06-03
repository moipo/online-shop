from .models import Order, OrderItem


def get_cart(request):
    user = request.user
    if user.is_authenticated:
        cart, _ = Order.objects.get_or_create(customer=user, status="Cart")
        return cart
    return get_visitor_cart(request)


def get_visitor_cart(request):
    if not request.session.session_key:
        request.session.create()
        request.session.save()

    session_key = request.session.session_key
    cart, created = Order.objects.get_or_create(
        session_key=session_key, status="Cart", customer=None
    )
    return cart

def merge_visitor_and_user_carts(request, user):
    # adds visitor's cart items to a user cart and deletes a visitor cart

    visitor_cart = get_visitor_cart(request)
    visitor_cart_items = OrderItem.objects.filter(order=visitor_cart)
    user_cart, _ = Order.objects.get_or_create(customer=user, status="Cart")
    user_cart_items = user_cart.orderitem_set.all()
    user_cart_products = [item.product for item in user_cart_items]

    for item in visitor_cart_items:
        if item.product in user_cart_products:
            user_cart_item = user_cart_items.get(product=item.product)
            user_cart_item.quantity += item.quantity
            user_cart_item.save()
        item.order = user_cart
        item.save()
    visitor_cart.delete()
