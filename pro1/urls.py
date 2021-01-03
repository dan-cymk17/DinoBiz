"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name="home"),
    path('logout/',views.Logoutuser,name="logout"),
    path('customer/<str:c_pk>/',views.test2,name="customer"),
    path('seller/',views.test1,name="seller"),
    path('order_update/<str:pk>/',views.orderUpdate,name="orderUpdate"),
    path('uhome/', views.userHome, name="uHome"),
    path('uprofile/', views.userProfile, name="uProfile"),
    path('sellerpage/<str:pk>/', views.order, name="order"),
    path('usercart/', views.cart, name="cart"),
    path('updatecart/', views.updateItem, name="updatecart"),
    path('orders/', views.vieworders, name="orders"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('sellerlogin/', views.sellerlogin, name="sellerlogin"),
    path('register/', views.register, name="register"),
    path('sprofile/', views.sellerProfile, name="sProfile"),
    path('productsAdd/', views.productsAdd, name="productsAdd"),
    path('p_update/<str:pk>/', views.productsUpdate, name="productsUpdate"),
    path('viewprod/', views.viewProducts, name="viewProducts"),
    path('delete_p/<str:pk>/', views.deleteproduct, name="deleteprod"),
    path('orderdetails/<str:pk>/', views.orderdetails, name="orderdetails"),
    path('updatestatus/<str:pk>/', views.updatestatus, name="updatestatus"),
    path('allorders/', views.allorders, name="allorders"),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
