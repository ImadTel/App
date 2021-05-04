from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from .models import Product


def products(request):

    context = {
        'products_list': Product.objects.all()
    }

    return render(request,"home-page.html",context)


def checkout(request):
   # return HttpResponse(request,"checkout-page.html")
   return render(request,"checkout-page.html")
