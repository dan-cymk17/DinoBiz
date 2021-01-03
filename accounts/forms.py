from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields=['customer','status']

class SellerUpdate(ModelForm):
    class Meta:
        model = Seller
        fields=['fname','lname','company','email','s_phone','description','image']
        labels = {
            'fname':_('First Name',),
            'lname':_('Last Name',),
            'company':_('Company',),
            'email':_('Email ID',),
            's_phone':_('Mobile Number',),
            'description':_('Description',),
            'image':_('Business Logo',),
        }
        help_texts = {
            'fname': _('Cannot contain Numbers or Special Characters'),
            'lname': _('Cannot contain Numbers or Special Characters'),
            'email': _('Enter valid personal email address'),
            's_phone': _('10 digit Mobile Number'),
            'description': _('Enter a short description of your business'),
        }


         
class UserUpdate(ModelForm):
    class Meta:
        model = Customer
        fields=['fname','lname','email','u_phone','profile']
        labels = {
            'fname':_('First Name',),
            'lname':_('Last Name',),
            'email':_('Email ID',),
            'u_phone':_('Mobile Number',),
            'profile':_('Profile Picture',),
        }
        help_texts = {
            'fname': _('Cannot contain Numbers or Special Characters'),
            'lname': _('Cannot contain Numbers or Special Characters'),
            'email': _('Enter valid personal email address'),
            'u_phone': _('10 digit Mobile Number'),
        }

class Shipping(ModelForm):
    class Meta:
        model = Delivery
        fields=['dno','street','locality','pincode']
        labels = {
            'dno':_('Flat/Door Number',),
            'street':_('Street',),
            'locality':_('Locality',),
            'pincode':_('Pincode',),
        }
        help_texts = {
            'locality': _('Adding a landmark would be Helpful'),
        }

class StatusUpdate(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': _('Status')
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description','image']
        labels = {
            'name': _('Product Name'),
            'price': _('Price per item'),
            'category': _('Category'),
            'description': _('Description')
        }


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description','image']
        labels = {
            'name': _('Product Name'),
            'price': _('Price per item'),
            'category': _('Category'),
            'description': _('Description')
        }
