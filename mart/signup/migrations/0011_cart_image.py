# Generated by Django 5.1 on 2024-09-15 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0010_remove_cart_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cart_images/'),
        ),
    ]
