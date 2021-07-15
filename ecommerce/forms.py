from django import forms
from django.db.models import fields
from django.forms.widgets import CheckboxInput, Widget
from .models import Product
from django_countries.fields import CountryField
'''
 title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(choices=CATEGORIES, max_length=2)
    price = models.FloatField(default=0)
    discout_price = models.FloatField(null=True,blank=True)
    label  = models.CharField(choices=LABELS,max_length=15)
    slug = models.SlugField()
'''

PAYEMENT = (
    ('pl','paypal'),
    ('cr','credit cart'),
    ('dc', 'debit cart')
)


class productForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['title','description','category','price',]



class CheckOutForm(forms.Form):
    street_adress = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        
        'id':'street_adress',
        } ))

    apartment = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        
        'id':'apartment',
    }))

  
    country = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={
        'class':'custom-select d-block w-100',
        
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        
        'id':'zip',
    }))

    same_billing_adress = forms.BooleanField(required=False)

    save_info = forms.BooleanField(required=False)

    payment_options = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYEMENT)
    