from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#creating a tag to identify the type of product/Service
class Tag(models.Model):
    Category =(
            ('Food' , 'Food'),
            ('Home Made' , 'Home Made'),
            ('Laundry' ,'Laundry'),
            ('Grocery' , 'Grocery'),
            ('Dessert','Dessert'),
            ('Art','Art'),
            ('Craft','Craft')
    ) 
    tag = models.CharField(max_length=200,null=True,choices=Category)

    def __str__(self):
        return self.tag


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200,null=True)
    lname = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    u_dob = models.DateField(null=True)
    u_phone = models.CharField(max_length=12,null=True)
    profile=models.ImageField(null=True,blank=True,upload_to="images/",default='default/image.jpg')
    date_created = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.fname

class Seller(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200,null=True)
    lname = models.CharField(max_length=200,null=True)
    company = models.CharField(max_length=100,null=True)
    address=  models.CharField(max_length=300,null=True)
    locality = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=200,null=True,)
    s_dob = models.DateField(null=True)
    s_phone = models.CharField(max_length=12,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    image=models.ImageField(null=True,blank=True,upload_to="images/")
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return self.company



class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    image=models.ImageField(null=True,blank=True,upload_to="images/product/",default='default/product.jpg')
    category = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    

    def __str__(self):
        return self.name

class Order(models.Model):
    #creating options for the status name and value
    STATUS =(
            ('Pending' , 'Pending'),
            ('Ready for Pickup' ,'Ready for Pickup'),
            ('Delivered' , 'Delivered'),
    ) 
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200,null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    t_id = models.CharField(max_length=200,null=True)

    @property
    def get_cart_total(self):
        orderitems= self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems= self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total


    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL,blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    
    @property
    def get_total(self):
        total =self.product.price * self.quantity
        return total
    
class Cart(models.Model):
    #creating options for the status name and value
    STATUS =(
            ('Pending' , 'Pending'),
            ('Ready for Pickup' ,'Ready for Pickup'),
            ('Delivered' , 'Delivered'),
    ) 
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    @property
    def get_cart_items(self):
        cartitems= self.cartitem_set.all()
        total=sum([item.quantity for item in cartitems])
        return total

    @property
    def get_cart_total(self):
        cartitems= self.cartitem_set.all()
        total=sum([item.get_total for item in cartitems])
        return total


    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL,blank=True)
    order = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL,blank=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)

    @property
    def get_total(self):
        total =self.product.price * self.quantity
        return total

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    dno = models.IntegerField(blank=True)
    street = models.CharField(max_length=200,blank=True)
    locality = models.CharField(max_length=200,blank=True)
    pincode = models.IntegerField(blank=True)