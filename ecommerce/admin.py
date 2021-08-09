from django.contrib import admin

# Register your models here.
from .models import Product,OrderProduct,Order,BillingAdress,Comment,Image

class ImageInline(admin.TabularInline):
    model=Image

class ProductConfig(admin.ModelAdmin):
    inlines = [ImageInline,]



admin.site.register(Product,ProductConfig)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(BillingAdress)
admin.site.register(Comment)
admin.site.register(Image)

