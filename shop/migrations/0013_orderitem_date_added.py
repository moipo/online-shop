# Generated by Django 4.1.3 on 2022-11-28 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_card_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
