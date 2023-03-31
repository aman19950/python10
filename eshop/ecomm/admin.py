from http.client import PROCESSING
from django.contrib import admin

from .models import Product, Category, Customer_Signup, order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryProduct(admin.ModelAdmin):
    list_display = ['name']


class CustomerSignup(admin.ModelAdmin):
    list_display = ['first_name']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, CategoryProduct)
admin.site.register(Customer_Signup, CustomerSignup)
admin.site.register(order)

# Register your models here.
