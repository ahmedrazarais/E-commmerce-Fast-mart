from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password

# MODEL FOR ACCOUNT DATA OF USERS
class Accounts_Table(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, validators=[MinLengthValidator(5)])
    username = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(4)])
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    security = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    address = models.CharField(default="",max_length=50, null=False, blank=False)

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


# MODEL FOR HISTORY
class History(models.Model):
    user = models.ForeignKey(Accounts_Table, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField(default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s History"


class Cart(models.Model):
    user = models.ForeignKey(Accounts_Table, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)  # Make it nullable
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField(default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def calculate_total_bill(self):
        if self.product_quantity is not None and self.price_per_unit is not None:
            return self.product_quantity * self.price_per_unit
        return 0.00

    def save(self, *args, **kwargs):
        self.total_bill = self.calculate_total_bill()
        super().save(*args, **kwargs)


# MODEL FOR CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name


# MODEL FOR PRODUCT
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
