from django.db import models
from django.utils.text import slugify
# Create your models here.


class Product(models.Model):
    CATEGORY = (
    ("Tech", "Tech"),
    ("New", "New"),
    ("Popular", "Popular"),
    )

    name = models.CharField(verbose_name = "Name_of_the_product" , max_length = 100)
    price = models.IntegerField()
    rating = models.IntegerField()
    # pic = models.ImageField(upload_to = "shop/%Y/%m")
    category = models.CharField(max_length = 100, choices = CATEGORY)
    slug = models.CharField(max_length = 100)

    def __repr__():
        return

    def get_absolute_url():
        return f"something"
# types of connection!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    products = models.ManyToManyField("Product")
