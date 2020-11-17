from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm

# Create your views here.
def home(request):
    return render(request,'welcome.html')


def test1(request,s_pk):
    seller= Seller.objects.get(id=s_pk)
    customer= Customer.objects.all()
    orders=seller.order_set.all()
    customer_names=orders.values('customer').distinct()
    c_name=[]
    for c in customer_names:
        c_name.append(customer.get(id=c['customer']))
    orders_count=orders.count()
    context ={'seller':seller,'orders':orders,'orders_count':orders_count,'c_name':c_name,'customer':customer}
    return render(request,'seller.html',context)

def test2(request,c_pk):
    customer= Customer.objects.get(id=c_pk)
    orders=customer.order_set.all()
    orders_count=orders.count()
    context ={'customer':customer,'orders':orders,'orders_count':orders_count}
    return render(request,'cus_details.html',context)

def orderUpdate(request,pk):
    order=Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method =='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/seller/'+str(order.seller.id))
    context = {'form':form}
    return render(request,'order_update.html',context)