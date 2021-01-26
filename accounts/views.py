from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import *
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            f_name=request.POST.get('username')
            user = User.objects.filter(username=f_name).first()
            print(user.username)
            new_customer = Customer(user=user,fname=f_name)
            print("done")
            new_customer.save()
            messages.success(request,"Your account has been Created, You can now login into your desired Account type!")
    context = {'form':form}
    return render(request,'welcome.html',context)

def userlogin(request):
    if request.method == 'POST':
        usr=request.POST.get('username')
        psd=request.POST.get('password')

        user = authenticate(request, username=usr, password=psd)

        if user is not None:
            login(request, user)
            return redirect('/uhome/')
        else:
            messages.info(request,"Username or Password Incorrect")
    return render(request,'userlogin.html')

def sellerlogin(request):
    if request.method == 'POST':
        usr=request.POST.get('username')
        psd=request.POST.get('password')

        user = authenticate(request, username=usr, password=psd)

        if user is not None:
            login(request, user)
            return redirect('/seller/')
        else:
            messages.info(request,"Username or Password Incorrect")
    return render(request,'sellerlogin.html')



def Logoutuser(request):
    logout(request)
    return redirect('/home/#login')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            f_name=request.POST.get('username')
            user = User.objects.filter(username=f_name).first()
            print(user.username)
            new_customer = Customer(user=user,f_name=f_name)
            print("done")
            new_customer.save()
            messages.success(request,"Your account has been Created, You can now login into your desired Account type!")
    context = {'form':form}
    return render(request,'register.html',context)

def test1(request):
    # seller= Seller.objects.get(id=s_pk)
    if request.user.is_authenticated:
        seller = request.user.seller

    customer= Customer.objects.all()
    orders=seller.order_set.all()
    customer_names=orders.values('customer').distinct()
    c_name=[]
    for c in customer_names:
        c_name.append(customer.get(id=c['customer']))
    orders_count=orders.count()
    pending_orders_count = orders.filter(status="Pending").count()
    context ={'seller':seller,'orders':orders,'orders_count':orders_count,'c_name':c_name,'customer':customer, 'pending_orders_count':pending_orders_count}
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


@login_required(login_url='userlogin')
def userHome(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************
    food=Product.objects.filter(category="Food")
    art=Product.objects.filter(category="Art")
    bites=Product.objects.filter(category="Quick Bites")
    seller=Seller.objects.all()
    order=customer.order_set.all()
    context={'user':customer,'seller':seller,'order':order,'food':food,'art':art,'bites':bites,'cartitems':cartitems}
    return render(request,'userhome.html', context)


@login_required(login_url='userlogin')
def userProfile(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        cart,created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartitems = cart.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************
    u_update=UserUpdate(instance=customer)
    order=customer.order_set.all()
    orders_count=order.count()
    context={'user':customer,'orders_count':orders_count,'u_form':u_update,'cartitems':cartitems}
    if request.method =='POST':
        u_update=UserUpdate(request.POST,request.FILES,instance=customer)
        if u_update.is_valid():
            u_update.save()
            messages.success(request,"Your profile has been updated Succesfully")
            return redirect('/uprofile/')
    return render(request,'userprofile.html',context)


@login_required(login_url='userlogin')
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

@login_required(login_url='userlogin')
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

@login_required(login_url='userlogin')
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

def sellerProfile(request):
    if request.user.is_authenticated:
        seller = request.user.seller
    # seller=Seller.objects.get(id=pk)
    s_update=SellerUpdate(instance=seller)
    # order=user.order_set.all()
    # orders_count=order.count()
    # context={'user':user,'orders_count':orders_count,'u_form':u_update}
    context={'seller':seller, 's_form':s_update}
    if request.method =='POST':
        s_update=SellerUpdate(request.POST,request.FILES,instance=seller)
        if s_update.is_valid():
            s_update.save()
            messages.success(request,"Your profile has been updated Succesfully")
            return redirect('/sprofile/')
    return render(request,'sellerprofile.html',context)

def viewProducts(request):
    if request.user.is_authenticated:
        seller = request.user.seller
    
    products = Product.objects.filter(seller=seller)
    context={'products':products}
    
    return render(request, 'viewProducts.html',context)

def productsAdd(request):
    if request.user.is_authenticated:
        seller = request.user.seller
    p_form = ProductForm()
    if request.method =='POST':
        p_form = ProductForm(request.POST)
        if p_form.is_valid():
            name = p_form.cleaned_data['name']
            price = p_form.cleaned_data['price']
            category = p_form.cleaned_data['category']
            descr = p_form.cleaned_data['description']
            p = Product(name=name, price=price, category=category, description=descr,seller=seller)
            p.save()
            messages.success(request,"Your profile has been updated Succesfully")
            return redirect('/viewprod/')
    context = {'user':seller, 'p_form':p_form}
    return render(request, 'products.html', context)

def productsUpdate(request,pk):
    if request.user.is_authenticated:
        seller=request.user.seller

    # else:
    #     items=[]
    #     order = {'get_cart_total':0,'get_cart_items':0}

    #******************************************************************************
    product = Product.objects.get(id=pk)
    p_update=ProductUpdateForm(instance=product)
    context = {'user':seller, 'p_update':p_update,'product':product}
    if request.method =='POST':
        p_update=ProductUpdateForm(request.POST,request.FILES,instance=product)
        if p_update.is_valid():
            p_update.save()
            messages.success(request,"Product has been updated")
            return redirect('/viewprod/')
    return render(request,'productsUpdate.html',context)

def deleteproduct(request,pk):
    if request.user.is_authenticated:
        seller=request.user.seller

    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/viewprod/')



def orderdetails(request,pk):
    if request.user.is_authenticated:
        seller=request.user.seller

    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()
    address=Delivery.objects.filter(order=order).first()
    print(address.dno)
    context ={'order':order,'items':items,'address':address}
    return render(request,'orderdetails.html',context)

def updatestatus(request,pk):
    if request.user.is_authenticated:
        seller=request.user.seller
    order = Order.objects.get(id=pk)
    order.status="Delivered"
    order.save()
    return redirect('/seller/') 

def allorders(request):
    if request.user.is_authenticated:
        seller=request.user.seller

    orders=seller.order_set.all()
    context={'orders':orders}
    return render(request,'allorders.html',context)