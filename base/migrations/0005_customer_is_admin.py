# Generated by Django 4.1.4 on 2024-03-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_product_description_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]