# Generated by Django 4.1.3 on 2023-01-24 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0018_alter_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
