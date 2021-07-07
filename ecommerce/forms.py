from django import forms
from django.db.models import fields
from .models import Product

'''
 title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(choices=CATEGORIES, max_length=2)
    price = models.FloatField(default=0)
    discout_price = models.FloatField(null=True,blank=True)
    label  = models.CharField(choices=LABELS,max_length=15)
    slug = models.SlugField()
'''


class productForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['title','description','category','price',]