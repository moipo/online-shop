from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import cart, detail

class TestUrls(SimpleTestCase):
    def test_cart_url(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)
        
    def test_detail_url(self):
        url = reverse('detail', args = ["some_slug"])
        self.assertEquals(resolve(url).func, detail)
        
        