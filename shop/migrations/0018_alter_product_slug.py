# Generated by Django 4.1.3 on 2023-01-24 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
