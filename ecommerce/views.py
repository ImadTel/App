
from django.shortcuts import render,get_object_or_404,redirect

from django.views.generic import ListView,DetailView

from django.utils import timezone


# Create your views here.
from .models import Product,Order,OrderProduct


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


def add_to_card(request,slug):
    product=get_object_or_404(Product,slug=slug)
    order_product = OrderProduct.objects.create(product=product.pk,quatity=request.quantity)

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product +=1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        order = Order.objects.create(user=request.user,order_date=timezone.now())
        order.products.add(order_product)
        order.save()
    return redirect("ecommerce:productDetail", slug=slug)


def add_to_cart(request,slug):
    product=get_object_or_404(Product,slug=slug)
    user_order=Order.objects.get_or_create(user=request.user,ordered=False,defaults={'orderedDate':timezone.now(), })

    Order.objects.get(ordered=False,user=request.user)

    defaults={}
    ord_prod = OrderProduct.objects.filter(product=product,order=user_order[0])
    if ord_prod.exists():
        print('ord_prod')
        print(ord_prod)
        quantity = int(request.POST['quantity']) + ord_prod[0].quantity
        defaults['quantity']=quantity
        print('q')
        print(defaults['quantity'])

    order_product = OrderProduct.objects.update_or_create(order=user_order[0],product=product,defaults=defaults)

    
    OrderProduct.objects.update()

    return redirect("ecommerce:productDetail", slug=slug)
        
