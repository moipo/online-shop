from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    CATEGORY = (
    ("Tech", "Tech"),
    ("New", "New"),
    ("Popular", "Popular"),
    )

    name = models.CharField(verbose_name = "название продукта" , max_length = 100)
    price = models.IntegerField()
    rating = models.IntegerField()
    pic = models.ImageField(upload_to = "shop/%Y/%m", null = True, blank = True, default = "default_picture.png")
    added_at = models.DateTimeField(auto_now_add = True, null = True)
    category = models.CharField(max_length = 100, choices = CATEGORY)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __repr__():
        return self.name

    def get_absolute_url(request):
        return f"products/{self.slug}"




class Order(models.Model):
    STATUS = (
    ("Pending", "Pending"),
    ("Ready", "Ready"),
    ("Delivered", "Delivered"),
    )

    date_created = models.DateTimeField(auto_now_add = True)
    products = models.ManyToManyField("Product")
    customer = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    status = models.CharField(choices = STATUS, default = "Pending", max_length = 255)

    def __repr__(self):
        return self.name



class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey("Product", null = True, blank = True )
    quantity = models.IntegerField()

    @property
    def total_item_price(self):
        return self.product.price * self.quantity
