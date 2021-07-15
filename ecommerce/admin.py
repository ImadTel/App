from django.contrib import admin

# Register your models here.
from .models import Product,OrderProduct,Order,BillingAdress

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(BillingAdress)
