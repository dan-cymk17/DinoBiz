from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import OrderForm,UserUpdate

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

def userHome(request,pk):
    user=Customer.objects.get(id=pk)
    food=Product.objects.filter(category="Food")
    art=Product.objects.filter(category="Art")
    bites=Product.objects.filter(category="Quick Bites")
    seller=Seller.objects.all()
    order=user.order_set.all()
    context={'user':user,'seller':seller,'order':order,'food':food,'art':art,'bites':bites}
    return render(request,'userhome.html', context)

def userProfile(request,pk):
    user=Customer.objects.get(id=pk)
    u_update=UserUpdate(instance=user)
    order=user.order_set.all()
    orders_count=order.count()
    context={'user':user,'orders_count':orders_count,'u_form':u_update}
    if request.method =='POST':
        u_update=UserUpdate(request.POST,request.FILES,instance=user)
        if u_update.is_valid():
            u_update.save()
            messages.success(request,"Your profile has been updated Succesfully")
            return redirect('/uprofile/'+str(user.id))
    return render(request,'userprofile.html',context)