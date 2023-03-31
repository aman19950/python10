from distutils.log import error
from math import prod
from tkinter.messagebox import NO
from warnings import catch_warnings
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from numpy import product

from torch import ge, rnn_relu
# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Category, Customer_Signup

# print(make_password('1234'))
# print(check_password(
#     '1234', 'pbkdf2_sha256$150000$Z6Iigx29THc9$ZQjloKgJBrAAGVhfYiIfOThPict32iONg48YSB1KB7Y='))


def index(request):
    products = None
    # request.session.clear()
    if request.method == "POST":
        product_id = request.POST.get('cartid')
        remove = request.POST.get('minus')
        cartid = request.session.get('cart')
        if cartid:
            quantity = cartid.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cartid.pop(product_id)
                    else:
                        cartid[product_id] = quantity - 1
                else:
                    cartid[product_id] = quantity + 1

            else:
                cartid[product_id] = 1

        else:
            cartid = {}
            cartid[product_id] = 1
        request.session['cart'] = cartid
        print(request.session['cart'])
        return redirect('home')

    cat = Category.get_all_cat()
    cat_id = request.GET.get('category')
    print(cat_id)

    if cat_id:
        products = Product.get_all_products_by_id(cat_id)
    else:
        products = Product.get_all_products()
    context = {
        'products': products,
        'cat': cat
    }
    # print(request.session.get('customer_email'))
    return render(request, 'home.html', context)


def validateCustomer(fname, lname, phone, email, password, con):
    error_message = None
    if(not fname):
        error_message = "First Name Required!!!"
    elif (len(fname)) < 4:
        error_message = 'First Name must be greater then 4'
    if(not lname):
        error_message = "Last Name Required!!!"
    elif (len(lname)) < 4:
        error_message = 'last Name must be greater then 4'
    elif(not phone):
        error_message = "Phone Number Required!!!"
    elif (len(phone)) < 10:
        error_message = 'Phone Number should be at least 10'
    elif(not password):
        error_message = "Password Required!!!"
    elif (len(password)) < 6:
        error_message = 'Password should be atleast 6 character'
    elif con.isExistsEmail():
        error_message = "Email already exists..."
    return error_message


def signup(request):

    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = None
        con = Customer_Signup(first_name=fname, last_name=lname,
                              phone=phone, gender=gender, email=email, password=password)
        # validation
        error_message = validateCustomer(
            fname, lname, phone, email, password, con)
        # if(not fname):
        #     error_message = "First Name Required!!!"
        # elif (len(fname)) < 4:
        #     error_message = 'First Name must be greater then 4'
        # if(not lname):
        #     error_message = "Last Name Required!!!"
        # elif (len(lname)) < 4:
        #     error_message = 'last Name must be greater then 4'
        # elif(not phone):
        #     error_message = "Phone Number Required!!!"
        # elif (len(phone)) < 10:
        #     error_message = 'Phone Number should be at least 10'
        # elif(not email):
        #     error_message = "Email Number Required!!!"
        # elif (len(phone)) < 5:
        #     error_message = 'Email must be at greater 5'
        # elif(not password):
        #     error_message = "Password Required!!!"
        # elif (len(password)) < 6:
        #     error_message = 'Password should be atleast 6 character'
        # elif con.isExistsEmail():
        #     error_message = "Email already exists..."
        if not error_message:
            # print(fname, lname, phone, email, gender, password)
            con.password = make_password(con.password)
            con.save()
            return redirect('home')
        else:
            return render(request, "home.html", {'error_message': error_message})


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = None

        cust_login = Customer_Signup.cust_login_by_email(email)
        if cust_login:
            request.session['customer_id'] = cust_login.id
            request.session['customer_email'] = cust_login.email
            flag = check_password(password, cust_login.password)
            if flag:
                return redirect('home')
            else:
                error_message = "Invalid password"
        else:
            error_message = "email is not exists"

    return render(request, 'home.html', {'error_message': error_message})


def cart(request):

    ids = list(request.session.get('cart').keys())
    prod = Product.get_pro_for_cart(ids)

    return render(request, 'cart.html', {'prod': prod})


def order(request):
    pass


def logout(request):
    request.session.clear()
    return redirect('home')
