# Generated by Django 5.1 on 2024-09-09 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_alter_cart_product_id_alter_history_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
