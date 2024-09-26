# Generated by Django 5.1 on 2024-09-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_alter_cart_price_per_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='history',
            name='product_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='history',
            name='total_bill',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
