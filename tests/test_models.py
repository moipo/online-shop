from django.test import TestCase

from shop.models import Order, OrderItem, Product


class TestModels(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="product", price=20)
        self.order = Order.objects.create(status="cart")

    def test_project_is_assigned_slug_on_creation(self):
        self.assertTrue(self.product.slug is not None)

    def test_total_item_price(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product)
        self.assertEquals(order_item.total_item_price, 0)
