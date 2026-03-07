from email.headerregistry import Address

from django.shortcuts import render, redirect
from AdminApp.models import CategoryDb, ProductDb
from WebApp.models import User_RegistrationDb, ContactDb, CartDb, OrderDb
from django.contrib import  messages
import razorpay

# Create your views here.

def home_page(request):
    categories = CategoryDb.objects.all()
    return render(request,"home.html",{"categories":categories})

def about_page(request):
    categories = CategoryDb.objects.all()
    return render(request,"about.html",{"categories":categories})

def all_products(request):
    products = ProductDb.objects.all()
    categories = CategoryDb.objects.all()
    latest_products = ProductDb.objects.order_by('-id')[:3]
    return render(request,"all_products.html",{"products":products,"categories":categories,"latest_products":latest_products})

def filtered_product(request,cat_name):
    products = ProductDb.objects.all()
    categories = CategoryDb.objects.all()
    latest_products = ProductDb.objects.order_by('-id')[:3]
    product = ProductDb.objects.filter(CategoryName=cat_name).all()
    return render(request,"filtered_products.html",{"products":products,"categories":categories,"product":product,"latest_products":latest_products})

def single_product(request,pro_id):
    categories = CategoryDb.objects.all()
    product = ProductDb.objects.get(id=pro_id)
    latest_products = ProductDb.objects.order_by('-id')[:3]
    return render(request,"single_product.html",{"product":product,"latest_products":latest_products,"categories":categories})

def sign_in(request):
    return render(request,"sign_in.html")

def sign_up(request):
    return render(request,"sign_up.html")

def save_user(request):
    if request.method == "POST":
        uname=request.POST.get("uname")
        email = request.POST.get("email")
        passwrd = request.POST.get("pswrd")
        con_pass = request.POST.get("cpswrd")
        if User_RegistrationDb.objects.filter(Username=uname).exists():
            # username already exist
            return redirect(sign_up)
        elif User_RegistrationDb.objects.filter(Email=email).exists():
            # email already exist
            return redirect(sign_up)
        else:
            obj = User_RegistrationDb(Username=uname,Email=email,Password=passwrd,Confirm_Password=con_pass)
            obj.save()
        return redirect(sign_up)

def user_login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pswrd = request.POST.get("pswrd")
        if User_RegistrationDb.objects.filter(Username=uname, Password=pswrd).exists():
            request.session['Username'] = uname
            request.session['Password'] = pswrd
            return redirect(home_page)
        else:
            return redirect(sign_in)

def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(home_page)

def contact(request):
    return render(request,"contact.html")

def save_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("phone")
        email = request.POST.get("email")
        subject = request.POST.get("sub")
        message = request.POST.get("msg")
        obj = ContactDb(Name=name,Mobile=mobile,Email=email,Subject=subject,Message=message)
        obj.save()
        return redirect(contact)

def help_page(request):
    return render(request,"help_page.html")

def support_page(request):
    return render(request,"support_page.html")

def cart(request):
    carts = CartDb.objects.filter(Username=request.session['Username'])
    subtotal = 0
    shipping_charge = 0
    total = 0
    for i in carts:
        subtotal += i.Total_price

        if subtotal > 100000:
            shipping_charge = 0

        elif subtotal >50000:
            shipping_charge = 100
        else:
            shipping_charge = 250

        total = subtotal + shipping_charge

    return render(request,"cart.html",{"carts":carts,"subtotal":subtotal,"shipping_charge":shipping_charge,"total":total})

def delete_cart_product(request,p_id):
    data = CartDb.objects.filter(id=p_id)
    data.delete()
    messages.success(request,"product deleted successfully")
    return redirect(cart)

def save_to_cart(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        qnty = request.POST.get("qnty")
        pro_name = request.POST.get("pro_name")
        price = request.POST.get("price")
        total = request.POST.get("total")
        obj = CartDb(Username=uname,Quantity=qnty,Price=price,Total_price=total,
                     Product_name=pro_name)
        obj.save()
        return redirect(home_page)

def checkout(request):
    carts = CartDb.objects.filter(Username=request.session['Username'])
    subtotal = 0
    shipping_charge = 0
    total = 0
    for i in carts:
        subtotal += i.Total_price

        if subtotal > 100000:
            shipping_charge = 0
        elif subtotal > 50000:
            shipping_charge = 100
        else:
            shipping_charge = 250

        total = subtotal + shipping_charge
    return render(request,"checkout.html",{"carts":carts,"subtotal":subtotal,"total":total,"shipping_charge":shipping_charge})

def save_order(request):
    if request.method == "POST":
        full_name = request.POST.get("fname")
        uname = request.POST.get("uname")
        total = request.POST.get("total")
        place = request.POST.get("place")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        message = request.POST.get("msg")
        pin = request.POST.get("pin")
        email = request.POST.get("email")
        obj = OrderDb(Username=uname,Full_name=full_name,Total_price=total,
                      Place=place,Mobile=mobile,Address=address,Message=message,
                      Pincode=pin,Email=email)
        obj.save()
        return redirect(checkout)


def payment_page(request):
    categories = CategoryDb.objects.all()
    for category in categories:
        count = ProductDb.objects.filter(Category_name=category.Category_name).count()
        category.product_count = count
    # payment details
    # Retrieve the data from CheckoutDB with specific ID
    customer = OrderDb.objects.order_by('-id').first()
    pay = customer.Total_price
    amount = int(pay * 100)
    pay_str = str(amount)
    if request.method == "POST":
        order_currency = "INR"
        client = razorpay.Client(auth=('rzp_test_0ib0jPwwZ7I1lT', 'VjHNO5zKeKxz8PYe7VnzwxMR'))  # KEY ID, Key sceret
        payment = client.order.create({
            'amount': amount,
            'currency': order_currency
        })

    return render(request, "payment.html", {"categories": categories,
                                            'pay_str': pay_str,
                                            'amount': amount})
