from django.db import models

# Create your models here.

#creating a tag to identify the type of product/Service
class Tag(models.Model):
    Category =(
            ('Food' , 'Food'),
            ('Home Made' , 'Home Made'),
            ('Laundry' ,'Laundry'),
            ('Grocery' , 'Grocery'),
            ('Dessert','Dessert'),
    ) 
    tag = models.CharField(max_length=200,null=True,choices=Category)

    def __str__(self):
        return self.tag


class Customer(models.Model):
    fname = models.CharField(max_length=200,null=True)
    lname = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    u_dob = models.DateField(null=True)
    u_phone = models.CharField(max_length=12,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.fname

class Seller(models.Model):
    fname = models.CharField(max_length=200,null=True)
    lname = models.CharField(max_length=200,null=True)
    company = models.CharField(max_length=100,null=True)
    address=  models.CharField(max_length=300,null=True)
    email = models.CharField(max_length=200,null=True)
    s_dob = models.DateField(null=True)
    s_phone = models.CharField(max_length=12,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    #add a many to many tag from tag
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return self.company



class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    #photo
    category = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    
    

    def __str__(self):
        return self.name

class Order(models.Model):
    #creating options for the status name and value
    STATUS =(
            ('Pending' , 'Pending'),
            ('Out for delivery' , 'Out for delivery'),
            ('Ready for Pickup' ,'Ready for Pickup'),
            ('Delivered' , 'Delivered'),
    ) 
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200,null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True,null=True)


    
