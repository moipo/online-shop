# Generated by Django 4.1.2 on 2022-11-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_pic_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Ready', 'Ready'), ('Delivered', 'Delivered'), ('Cart', 'Cart')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data of appearance'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]