from django.contrib import admin
from .models import Accounts_Table,History,Category,Product,Cart
# Register your models here.

admin.site.register(Accounts_Table)

admin.site.register(History)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Product)
