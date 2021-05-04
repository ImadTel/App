from django.contrib import admin

# Register your models here.
from .models import Product,OrderProduct,Order

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)

