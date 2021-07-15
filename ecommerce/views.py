
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect

from django.views.generic import ListView,DetailView,UpdateView

from django.views import View

from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from django.contrib import messages

from django.shortcuts import reverse

from django.contrib.auth.decorators import login_required

from .tasks import return_somthing,send_email_task

from django.core.mail import send_mail

from django.conf import settings

from .models import CATEGORIES,BillingAdress

from .forms import CheckOutForm

import stripe

from django.conf import settings

# Create your views here.
from .models import Product,Order,OrderProduct

from django.http import HttpResponse






def products(request):

    context = {
        'products_list': Product.objects.all()
    }

    return render(request,"home-page.html",context)




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
def add_to_cart(request,slug,**kwargs):
    #return_somthing.apply_async()
    #send_email_task.apply_async()    
    #send_email_task()

    
    if  kwargs:
        
        product=get_object_or_404(Product,slug=slug)
        ord = get_object_or_404(Order,user=request.user,ordered=False)
        ord_prod = get_object_or_404(OrderProduct,order=ord,product=product)
        ord_prod.quantity=quantity=ord_prod.quantity+ int(kwargs["quantity"])
        if ord_prod.quantity==0:
            ord_prod.delete()
        else:
            ord_prod.save()


        print ('task called')
       
        
        return redirect("ecommerce:cart_view")



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
    pro=Product.objects.all()
    for p in pro:
        print (p.get_add_one_to_cart_url())

    context = {}
    if request.user.is_authenticated:
        
        order= Order.objects.filter(user=request.user,ordered=False)
        if order.exists():
           

            context['objects']=order[0].get_linked_products()
            context['productsNumber']=context['objects'].count()
            context['total']=order[0].get_total_coast()
            return render(request,"cart.html",context)
        else:
            messages.add_message(request,messages.WARNING,"your cart is empty")
            return redirect("ecommerce:home") 
    else:
        
        messages.add_message(request,messages.ERROR,"you are not authenticated")
        return redirect("ecommerce:home")          
        

class update_view(UpdateView):
     model = Product
     template_name = 'update.html'
     fields = ['title','category','price','discout_price','description','label']

     def get_context_data(self, **kwargs):

         context = super().get_context_data(**kwargs)
         
         context['categories']=dict(CATEGORIES)
         return context


def remove_product_from_cart(request,slug):
    if request.user.is_authenticated:
        message=""
        order = Order.objects.filter(user=request.user,ordered=False)
        if order.exists():
            orderProduct = OrderProduct.objects.filter(order=order[0].id,product__slug=slug)
            if orderProduct.exists():
                orderProduct.delete()
                message = "Product order has been deleted from your cart"
        return redirect("ecommerce:cart_view")




def checkout(request):
   # return HttpResponse(request,"checkout-page.html")
   return render(request,"checkout-page.html")





class Checkout_view(View):
    
    def get(self,*args,**kwargs):
        if (self.request.user.is_authenticated):
            form = CheckOutForm()
            context= {
             'form':form
             }
            return render(self.request,"checkout-page.html",context)
        else:
            messages.add_message(self.request,messages.WARNING,"you are not authenticated")
            return redirect("ecommerce:home")



    def post(self,*args,**kwargs):
        form = CheckOutForm(self.request.POST or None)
        print(self.request.POST)

        if (self.request.user.is_authenticated):
            if form.is_valid():
                order = Order.objects.get(user=self.request.user,ordered=False)
                
                
                
                
                street_adress = form.cleaned_data.get('street_adress')
                apartment  = form.cleaned_data.get('apartment')
                country = form.cleaned_data.get('country')
                zipe = form.cleaned_data.get('zip')
                same_billing_adress = form.cleaned_data.get('same_billing_adress')
                save_info = form.cleaned_data.get('save_info')
                payment_options = form.cleaned_data.get('payment_options')
                
                
                billing_adress = BillingAdress(order=order, user=order.user,
                street_Adress=street_adress,
                apartment=apartment,
                country=country,
                zip=zipe

                )
                  # if user has already a saved adress we update it  
              
                bilAd=BillingAdress.objects.filter(order=order)
                
                
                if (bilAd.exists()):
                    messages.success(self.request,"your adress has been updated")
                    instance=BillingAdress.objects.get(order=order)
                    instance.street_Adress = street_adress
                    instance.user = order.user
                    instance.apartment = apartment
                    instance.country = country
                    instance.zip = zipe
                    instance.save()
                else : 
                     messages.success(self.request,"your adress has been saved")   
                     billing_adress.save()
                    
                print(same_billing_adress)
                YOUR_DOMAIN = 'http://127.0.0.1/ecommerce'

                
                order = Order.objects.get(user=self.request.user, ordered=False) 
                print(order)
                products = OrderProduct.objects.filter(order=order)

                items = []
                for item in products:

                    print (int(item.product.price*100))
                    print (item.product.title)
                    print (item.quantity)


                    prod= {

                    'price_data': {

                        'currency': 'usd',

                        'unit_amount': str(int(item.product.price*100)),

                        'product_data': {

                            'name': item.product.title,

                            #'images': ['https://i.imgur.com/EHyR2nP.png'],

                        },

                    },

                    'quantity':str(int(item.quantity)),

                }

                    items.append(prod)
            
        
        
                checkout_session = stripe.checkout.Session.create(

                payment_method_types=['card'],

                line_items=items,

                mode='payment',

                success_url=YOUR_DOMAIN + '/success',

                cancel_url=YOUR_DOMAIN + '/cancel',

                )
   
            return redirect(checkout_session.url, code=303)
        
        else:
            messages.add_message(self.request,messages.DANGER,"form is not valid") 
            return redirect("ecommerce:checkout")
        

class PayementView(View):

    def get(self,*args,**kwargs):

        return render(self.request,'payment.html')






stripe.api_key = settings.STRIPE_TEST_SECRET_KEY





class CreateCheckoutSession(View):

    def post(self,*args,**kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1/ecommerce'

        user_id=self.request.POST["user"]
        order = Order.objects.get(user__id=user_id, ordered=False) 
    
        products = OrderProduct.objects.filter(order=order)

        items = []
        for item in products:
          


            prod= {

                    'price_data': {

                        'currency': 'usd',

                        'unit_amount': str(int(item.product.price*100)),

                        'product_data': {

                            'name': item.product.title,

                            #'images': ['https://i.imgur.com/EHyR2nP.png'],

                        },

                    },

                    'quantity':str(int(item.quantity)),

                }

            items.append(prod)
            
        print(items)
        
        checkout_session = stripe.checkout.Session.create(

            payment_method_types=['card'],

            

            line_items=items,

            mode='payment',

            success_url=YOUR_DOMAIN + '/success',

            cancel_url=YOUR_DOMAIN + '/cancel',

        )
   
        return redirect(checkout_session.url, code=303)




def success_payment(request,*args,**kwargs):
     return render(request,'success.html')
 
 
 
def cancel_payment(request,*args,**kwargs):
     return render(request,'cancel.html')




def fulfill_order(session):
  # TODO: fill me in
    print("Fulfilling order")
  # Passed signature verification
    return HttpResponse(status=200)


endpoint_secret = settings.WH_SECRET


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print('i  m here')
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)

  # Passed signature verification
    return HttpResponse(status=200)



  