from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import OrderForm,UserUpdate,Shipping
from django.http import JsonResponse
import json

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
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************
    customer=Customer.objects.get(id=pk)
    food=Product.objects.filter(category="Food")
    art=Product.objects.filter(category="Art")
    bites=Product.objects.filter(category="Quick Bites")
    seller=Seller.objects.all()
    order=customer.order_set.all()
    context={'user':customer,'seller':seller,'order':order,'food':food,'art':art,'bites':bites,'cartitems':cartitems}
    return render(request,'userhome.html', context)

def userProfile(request,pk):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************


    user=Customer.objects.get(id=pk)
    u_update=UserUpdate(instance=user)
    order=user.order_set.all()
    orders_count=order.count()
    context={'user':user,'orders_count':orders_count,'u_form':u_update,'cartitems':cartitems}
    if request.method =='POST':
        u_update=UserUpdate(request.POST,request.FILES,instance=user)
        if u_update.is_valid():
            u_update.save()
            messages.success(request,"Your profile has been updated Succesfully")
            return redirect('/uprofile/'+str(user.id))
    return render(request,'userprofile.html',context)

def order(request,pk):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************


    seller=Seller.objects.get(id=pk)
    products=Product.objects.filter(seller=seller)
    orders=seller.order_set.all()
    orders_count=orders.count()
    context={'seller':seller,'orders':orders,'orders_count':orders_count,'products':products,'cartitems':cartitems}
    return render(request,'sellerpage.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}
    #******************************************************************************
    d_form = Shipping( )
    if request.method == 'POST':
        d_form = Shipping(request.POST)
        if d_form.is_valid():
            messages.success(request,"Order has been Sucessfully Placed")
            new_order = Order(customer=customer,seller=cart.seller,status="Pending")
            new_order.save()
            for i in items:
                new_item=OrderItem(product=i.product,order=new_order,quantity=i.quantity)
                new_item.save()
                i.delete()
            d_form.save()
            d_mod = Delivery.objects.filter(dno=d_form.data['dno'],street=d_form.data['street'],locality=d_form.data['locality']).first()
            d_mod.order= new_order
            d_mod.save()
            cart.delete()            
            return redirect('/orders/')

    context={'items':items,'cart':cart,'cartitems':cartitems,'d_form':d_form}
    return render(request,'usercart.html',context)

def vieworders(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}


    customer=request.user.customer
    orders= Order.objects.filter(customer=customer).order_by('-date_created')
    context={'orders':orders,'cartitems':cartitems}
    return render(request,'orders.html',context)



def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order= Cart.objects.filter(customer=customer).first()
    order.seller= product.seller
    order.save()
    orderitem,created = CartItem.objects.get_or_create(product=product,order=order)
    if action =='add':
        orderitem.quantity = orderitem.quantity+1
    #add an elif later for removing
    elif action == 'remove':
        orderitem.quantity = orderitem.quantity-1

    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    if order.get_cart_items == 0:
        Cart.objects.filter(customer=customer).delete()

    print(productId,action)
    return JsonResponse('Item was added', safe=False)