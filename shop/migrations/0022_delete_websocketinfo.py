# Generated by Django 4.1.3 on 2024-06-04 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0021_order_session_key"),
    ]

    operations = [
        migrations.DeleteModel(
            name="WebsocketInfo",
        ),
    ]
