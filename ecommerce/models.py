from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django_countries.fields import CountryField


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
    image = models.ImageField(upload_to='products',blank=True,null=True)
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

    def get_update_url(self):
        return reverse('ecommerce:update_item',kwargs ={
            'pk' : self.pk,
        })

    def get_add_one_to_cart_url(self):
        return reverse('ecommerce:cart_view_res',kwargs ={
            'slug' : self.slug,
            'quantity' : 1,
        })
    def get_subs_one_to_cart_url(self):
        return reverse('ecommerce:cart_view_res',kwargs ={
            'slug' : self.slug,
            'quantity' : -1,
        })

    
    def get_remove_from_cart_url(self):
        return reverse('ecommerce:remove_from_cart',kwargs={
            'slug':self.slug,
        })

    def remove_product_from_cart_view_url(self):
        return reverse('ecommerce:remove_product_from_cart_view',kwargs={
            'slug':self.slug,
        })




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    orderedDate = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_linked_products(self):
        return OrderProduct.objects.filter(order=self)


    def get_total_coast(self):
        prods = self.get_linked_products()
        total=0
        for prod in prods:
            if not prod.product.discout_price:
                total += prod.product.price * prod.quantity
            else:
                total += prod.product.discout_price * prod.quantity
        return total


class OrderProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    def __str__(self):
        return self.product.title + '  ' + str(self.quantity)


 

class BillingAdress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    street_Adress =models.CharField(max_length=200)
    apartment = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=50)
    order = models.ForeignKey(Order,on_delete=CASCADE)
    


class Comment(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    product = models.ForeignKey(Product,on_delete=CASCADE)
    rating = models.IntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return self.content  + ';  user: ' + self.user.username + '; product: ' + self.product.title
