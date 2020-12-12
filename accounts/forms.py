from django.forms import ModelForm
from .models import Order,Customer,Seller,Delivery
from django.utils.translation import gettext_lazy as _


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields=['customer','status']
         
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