
from statistics import mode
from unicodedata import category
from django.db import models
import datetime
# from validators import email

# from . models import Category
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    subcat = models.CharField(max_length=50)

    @staticmethod
    def get_all_cat():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='uploads/products/')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)

    @staticmethod
    def get_pro_for_cart(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Customer_Signup(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    @staticmethod
    def cust_login_by_email(email):
        try:
            return Customer_Signup.objects.get(email=email)
        except:
            return False

    def isExistsEmail(self):
        if Customer_Signup.objects.filter(email=self.email):
            return True
        return False


class order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer_Signup, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
