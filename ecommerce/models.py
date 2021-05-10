from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

CATEGORIES = [
    ('Cp', 'computers'),
    ('MB', 'mobiles'),
    ('TB', 'Tablettes'),
]

LABELS = [
    ('primary','Gaming'),
    ('secondary','Photofraphie'),
    ('danger','Normal'),
    ('warning','Low Caost'),
]


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(choices=CATEGORIES, max_length=2)
    price = models.FloatField(default=0)
    discout_price = models.FloatField(null=True,blank=True)
    label  = models.CharField(choices=LABELS,max_length=15)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ecommerce:productDetail',kwargs ={
            'slug' : self.slug,
        })

    def get_add_to_cart_url(self):
        return reverse('ecommerce:add_to_cart',kwargs ={
            'slug' : self.slug,
        })

    
    def get_remove_from_cart_url(self):
        return reverse('ecommerce:remove_from_cart',kwargs={
            'slug':self.slug,
        })




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    orderedDate = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_linked_products_number(self):
        return OrderProduct.objects.filter(order=self).count()



class OrderProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    def __str__(self):
        return self.product.title + '  ' + str(self.quantity)


