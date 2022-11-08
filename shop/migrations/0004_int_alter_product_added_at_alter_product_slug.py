# Generated by Django 4.1.2 on 2022-11-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_pic_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Int',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
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
