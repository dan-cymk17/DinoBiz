from django.contrib import admin

# Register your models here.
#can also use * to import all models
from .models import *

admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Delivery)

 
