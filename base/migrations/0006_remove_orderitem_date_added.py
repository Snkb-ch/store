# Generated by Django 4.1.4 on 2024-03-05 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_customer_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='date_added',
        ),
    ]
