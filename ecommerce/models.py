from django.db import models
from django.conf import settings
# Create your models here.


class Product(models.Model):
    title=models.CharField(max_length=100)
    description = models.CharField(max_length=500)


    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    order_date = models.DateTimeField(auto_now_add=True)
    orderedDate = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
