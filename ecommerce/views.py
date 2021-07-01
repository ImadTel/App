
from django.shortcuts import render,get_object_or_404,redirect

from django.views.generic import ListView,DetailView

from django.utils import timezone

from django.contrib import messages

from django.shortcuts import reverse

from django.contrib.auth.decorators import login_required



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


#class productView(ListView):
#   model = Product
#  template_name = "home-page.html"


class productView(ListView):
    model = Product
    template_name = "home-page.html"
    paginate_by = 2
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['productsNumber'] = 0
        print (self.request.user)
        
        if self.request.user.is_authenticated:
            ord =Order.objects.filter(user=self.request.user,ordered=False)
            if ord.exists():
                productsInCart = ord[0].get_linked_products().count()
                context['productsNumber'] = productsInCart
        return context



class productDetail(DetailView):
    model=Product
    template_name = "product-page.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['productsNumber'] = 0
        print (self.request.user)
        
        if self.request.user.is_authenticated:
            ord =Order.objects.filter(user=self.request.user,ordered=False)
            if ord.exists():
                productsInCart = ord[0].get_linked_products().count()
                context['productsNumber'] = productsInCart
        return context

        
@login_required
def add_to_cart(request,slug):
    if    request.POST.get('quantity')==None:
        return redirect("ecommerce:productDetail",slug=slug)
    

    if int(request.POST.get('quantity'))<0:
        messages.add_message(request,messages.WARNING,"quantity should ne greater than 0")
        return redirect("ecommerce:productDetail",slug=slug)


    if request.user.is_authenticated:
        product=get_object_or_404(Product,slug=slug)
        user_order=Order.objects.get_or_create(user=request.user,ordered=False,defaults={'orderedDate':timezone.now(), })

        Order.objects.get(ordered=False,user=request.user)
        
        defaults={}
        defaults['quantity']=int(request.POST.get('quantity'))
        ord_prod = OrderProduct.objects.filter(product=product,order=user_order[0])
        message=""
        if ord_prod.exists():
            print('ord_prod')
            print(ord_prod)
            quantity = int(request.POST['quantity']) + ord_prod[0].quantity
            defaults['quantity']=quantity
            message="the product quantity has been updated"
            
        if message=="":
            message ="Product added succesfuly"
        order_product = OrderProduct.objects.update_or_create(order=user_order[0],product=product,defaults=defaults)
        messages.add_message(request,messages.SUCCESS,message)
        return redirect("ecommerce:productDetail",slug=slug)
    



def remove_from_cart(request,slug):
    if request.user.is_authenticated:
        message=""
        order = Order.objects.filter(user=request.user,ordered=False)
        if order.exists():
            orderProduct = OrderProduct.objects.filter(order=order[0].id,product__slug=slug)
            if orderProduct.exists():
                orderProduct.delete()
                message = "Product order has been deleted from your cart"
            else:
                message="This product doesn't exist in your cart"
        else:
            message="you do not have an order yet"
        
        messages.add_message(request,messages.WARNING,message)
        return redirect("ecommerce:productDetail",slug=slug)
    else:
        messages.add_message(request,messages.warning,"you are not authenticated")
        
        return redirect("/accounts/login")
    




def cart_view(request):
    context = {}
    if request.user.is_authenticated:
        print (request.user)
        order= Order.objects.filter(user=request.user,ordered=False)
        if order.exists():
            print ('hi')

            context['objects']=order[0].get_linked_products()
            context['productsNumber']=context['objects'].count()
            context['total']=order[0].get_total_coast()
            return render(request,"cart.html",context)
        else:
            messages.add_message(request,messages.WARNING,"your cart is empty")
            return redirect("ecommerce:home") 
    else:
        print ('ha')
        messages.add_message(request,messages.ERROR,"you are not authenticated")
        return redirect("ecommerce:home")          
        