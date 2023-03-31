from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name='home'),
    path("signup", views.signup, name='signup'),
    path("cart", views.cart, name='cart'),
    path("logout", views.logout, name='logout'),
    path("order", views.order, name='order'),
    path("login", views.login, name='login'),
    # path("/category ", views.index, name='home'),

]
