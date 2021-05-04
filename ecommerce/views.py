
from django.shortcuts import render
from django.views.generic import ListView,DetailView


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


class productView(ListView):
    model = Product
    template_name = "home-page.html"


class productView(ListView):
    model = Product
    template_name = "home-page.html"

class productDetail(DetailView):
    model=Product
    template_name = "product-page.html"




