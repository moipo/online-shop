# Generated by Django 4.1.3 on 2022-11-19 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_alter_order_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
