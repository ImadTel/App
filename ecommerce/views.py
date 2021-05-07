
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
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        productsInCart = OrderProduct.objects.filter(order=Order.objects.get(user=self.request.user,ordered=False)).count()
        context['productsNumber'] = productsInCart
        return context

        

def add_to_cart(request,slug):
    product=get_object_or_404(Product,slug=slug)
    user_order=Order.objects.get_or_create(user=request.user,ordered=False,defaults={'orderedDate':timezone.now(), })

    Order.objects.get(ordered=False,user=request.user)

    defaults={}
    defaults['quantity']=int(request.POST['quantity'])
    ord_prod = OrderProduct.objects.filter(product=product,order=user_order[0])
    if ord_prod.exists():
        print('ord_prod')
        print(ord_prod)
        quantity = int(request.POST['quantity']) + ord_prod[0].quantity
        defaults['quantity']=quantity
        
        

    order_product = OrderProduct.objects.update_or_create(order=user_order[0],product=product,defaults=defaults)

    
    OrderProduct.objects.update()

    return redirect("ecommerce:productDetail", slug=slug)
        


def remove_from_cart(request,slug):
    order = Order.objects.filter(user=request.user,ordered=False)
    if order.exists():
        orderProduct = OrderProduct.objects.filter(order=order[0].id,product__slug=slug)
        if orderProduct.exists():
            orderProduct.delete()
        else:
            print("you didn t order that product")
    else:
        print("you do not have an order yet")
    
    return redirect("ecommerce:productDetail",slug=slug)
    

