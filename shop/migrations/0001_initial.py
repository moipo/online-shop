# Generated by Django 4.1.2 on 2022-11-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Name_of_the_product"
                    ),
                ),
                ("price", models.IntegerField()),
                ("rating", models.IntegerField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Tech", "Tech"),
                            ("New", "New"),
                            ("Popular", "Popular"),
                        ],
                        max_length=100,
                    ),
                ),
                ("slug", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("products", models.ManyToManyField(to="shop.product")),
            ],
        ),
    ]
