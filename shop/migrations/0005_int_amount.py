# Generated by Django 4.1.2 on 2022-11-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_int_alter_product_added_at_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='int',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
