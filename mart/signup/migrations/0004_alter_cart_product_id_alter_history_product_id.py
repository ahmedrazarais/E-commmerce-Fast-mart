# Generated by Django 5.1 on 2024-09-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_alter_cart_total_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='product_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
