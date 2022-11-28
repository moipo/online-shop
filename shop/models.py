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

    default_description = """
    Eos no lorem eirmod diam diam, eos elitr et gubergren diam sea. Consetetur vero aliquyam invidunt duo dolores et duo sit. Vero diam ea vero et dolore rebum, dolor rebum eirmod consetetur invidunt sed sed et, lorem duo et eos elitr, sadipscing kasd ipsum rebum diam. Dolore diam stet rebum sed tempor kasd eirmod. Takimata kasd ipsum accusam sadipscing, eos dolores sit no ut diam consetetur duo justo est, sit sanctus diam tempor aliquyam eirmod nonumy rebum dolor accusam, ipsum kasd eos consetetur at sit rebum, diam kasd invidunt tempor lorem, ipsum lorem elitr sanctus eirmod takimata dolor ea invidunt.

    Dolore magna est eirmod sanctus dolor, amet diam et eirmod et ipsum. Amet dolore tempor consetetur sed lorem dolor sit lorem tempor. Gubergren amet amet labore sadipscing clita clita diam clita. Sea amet et sed ipsum lorem elitr et, amet et labore voluptua sit rebum. Ea erat sed et diam takimata sed justo. Magna takimata justo et amet magna et.
    """

    name = models.CharField(verbose_name = "название продукта" , max_length = 100)
    price = models.IntegerField(null = True, blank = True)
    description = models.TextField(default = default_description, blank = True)
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
    date_added = models.DateTimeField(auto_now = True, null = True, blank = True)

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
    date_added = models.DateTimeField(auto_now_add = True, null = True)

    def __repr__(self):
        return self.name

    @property
    def order_total_price(self):
        return sum([item.total_item_price for item in self.orderitem_set.all()])

    @property
    def order_total_quantity(self):
        return sum([item.quantity for item in self.orderitem_set.all()])



class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, blank = True, null = True, on_delete = models.SET_NULL)
    order = models.ForeignKey(Order, blank = True, null = True, on_delete = models.SET_NULL)
    country = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    address = models.CharField(max_length = 200, null = True)
    zip_code = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True, null = True)

    def __repr__(self):
        return self.address

class Card(models.Model):
    customer = models.ManyToManyField(User, blank = True)
    order = models.ForeignKey(Order, blank = True, null = True, on_delete = models.SET_NULL)
    name_on_card = models.CharField(max_length = 200, null = True)
    number = models.CharField(max_length = 200, null = True)
    expiration_date = models.CharField(max_length = 200, null = True)
    cvv = models.CharField(max_length = 200, null = True)
