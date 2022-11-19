from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from time import time
# Create your models here.


class Product(models.Model):
    CATEGORY = (
    ("Tech", "Tech"),
    ("New", "New"),
    ("Popular", "Popular"),
    )

    name = models.CharField(verbose_name = "название продукта" , max_length = 100)
    price = models.IntegerField(null = True, blank = True)
    description = models.TextField(default = "", blank = True)
    rating = models.IntegerField(null = True, blank = True)
    pic = models.ImageField(upload_to = "shop/%Y/%m", null = True, blank = True, default = "default_picture.png")
    added_at = models.DateTimeField(verbose_name = "Data of appearance", auto_now_add = True, null = True)
    category = models.CharField(max_length = 100, choices = CATEGORY)
    slug = models.SlugField(blank = True)




    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(time()) + "-" + self.name)
        super().save(*args, **kwargs)

    def __repr__():
        return self.name

    def get_absolute_url():
        return f"detail/{self.slug}"









class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete = models.CASCADE)
    product = models.ForeignKey("Product", null = True, blank = True, on_delete = models.CASCADE )
    quantity = models.IntegerField()

    @property
    def total_item_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS = (
    ("Pending", "Pending"),
    ("Ready", "Ready"),
    ("Delivered", "Delivered"),
    ("Cart", "Cart"),
    )

    date_created = models.DateTimeField(null = True)
    products = models.ManyToManyField("Product")
    customer = models.ForeignKey(User, blank = True, null = True, on_delete = models.SET_NULL)
    status = models.CharField(choices = STATUS, default = "Pending", max_length = 255)

    def __repr__(self):
        return self.name

    @property
    def order_total_price(self):
        return sum([item.total_item_price for item in self.orderitem_set.all()])

    @property
    def order_total_quantity(self):
        return sum([item.quantity for item in self.orderitem_set.all()])
