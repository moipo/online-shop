from django.db import transaction

from .models import Order, OrderItem


def get_cart(request, *, create=True):
    if request.user.is_authenticated:
        cart_query = Order.objects.filter(customer=request.user, status="Cart")
    else:
        return get_visitor_cart(request, create=create)

    cart = cart_query.order_by("pk").first()
    if cart is None and create:
        cart = Order.objects.create(customer=request.user, status="Cart")
    return cart


def get_visitor_cart(request, *, create=True):
    if not request.session.session_key:
        if not create:
            return None
        request.session.create()

    session_key = request.session.session_key
    cart_query = Order.objects.filter(
        session_key=session_key, status="Cart", customer=None
    )
    cart = cart_query.order_by("pk").first()
    if cart is None and create:
        cart = Order.objects.create(
            session_key=session_key,
            status="Cart",
            customer=None,
        )
    return cart


@transaction.atomic
def merge_visitor_and_user_carts(request, user):
    visitor_cart = get_visitor_cart(request, create=False)
    if visitor_cart is None:
        return

    visitor_cart_items = OrderItem.objects.filter(
        order=visitor_cart
    ).select_for_update()
    user_cart, _ = Order.objects.get_or_create(customer=user, status="Cart")
    user_cart_items = {
        item.product_id: item
        for item in user_cart.orderitem_set.select_for_update().all()
    }

    for item in visitor_cart_items:
        user_cart_item = user_cart_items.get(item.product_id)
        if user_cart_item is not None:
            user_cart_item.quantity = (user_cart_item.quantity or 0) + (
                item.quantity or 0
            )
            user_cart_item.save(update_fields=["quantity"])
        else:
            item.order_id = user_cart.pk
            item.save(update_fields=["order"])

    visitor_cart.delete()
