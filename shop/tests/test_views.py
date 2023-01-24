from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, OrderItem, Order
import json

class TestViews(TestCase):
    
    def setUp(self):
        tmp_order = Order.objects.create()
        self.client = Client()
        self.shop_url = reverse('shop')
        self.order_detail_url = reverse('order_detail', args = [tmp_order.id])
        self.api_change_cart_url = reverse('api_change_cart')
        
        self.product_id = Product.objects.create(name = "product")
        
        
        
    def test_index_GET(self):
        
        response = self.client.get(self.shop_url)
        
        self.assertEquals(response.status_code,  200)
        self.assertTemplateUsed(response, 'shop.html')
        
        
    def test_order_deitail_GET_forbidden(self):
        
        response = self.client.get(self.order_detail_url)
        
        self.assertEquals(response.status_code,  403)


    def test_api_cart_post_adds_new_item(self):
        OrderItem.objects.create()
        response = self.client.post(self.api_change_cart_url,
            {"product_id":self.product_id,
            "action":"add"
            })
        print(response)