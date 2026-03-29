from django.shortcuts import render, redirect
from AdminApp.models import CategoryDb, ProductDb
from WebApp.models import User_RegistrationDb, ContactDb, CartDb, OrderDb
from django.contrib import  messages
from django.conf import settings
from django.urls import reverse
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
    return render(request,"filtered_products.html",{"products":products,"categories":categories,"product":product,"latest_products":latest_products,"selected_category":cat_name})

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
    request.session.pop('Username', None)
    request.session.pop('Password', None)
    return redirect(home_page)

def contact(request):
    categories = CategoryDb.objects.all()
    return render(request,"contact.html", {"categories": categories})

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
    categories = CategoryDb.objects.all()
    username = request.session.get('Username')
    carts = CartDb.objects.filter(Username=username) if username else CartDb.objects.none()
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

    return render(request,"cart.html",{
        "carts":carts,
        "subtotal":subtotal,
        "shipping_charge":shipping_charge,
        "total":total,
        "categories":categories,
        "cart_user_logged_in": bool(username),
    })

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
    categories = CategoryDb.objects.all()
    username = request.session.get('Username')
    if not username:
        messages.error(request, "Please sign in to continue to checkout.")
        return redirect(sign_in)

    carts = CartDb.objects.filter(Username=username)
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
    return render(request,"checkout.html",{"carts":carts,"subtotal":subtotal,"total":total,"shipping_charge":shipping_charge,"categories":categories})

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
                      Pincode=pin,Email=email,Payment_status="Pending")
        obj.save()
        return redirect(payment_page)
    return redirect(checkout)


def payment_page(request):
    categories = CategoryDb.objects.all()
    for category in categories:
        count = ProductDb.objects.filter(CategoryName=category.Category_name).count()
        category.product_count = count

    username = request.session.get("Username")
    customer = OrderDb.objects.filter(Username=username).order_by('-id').first()
    if customer is None:
        messages.error(request, "Please place an order before continuing to payment.")
        return redirect(checkout)

    if customer.Payment_status == "Paid":
        messages.success(request, "This order has already been paid successfully.")
        return redirect(home_page)

    try:
        total_price = int(float(customer.Total_price))
    except (TypeError, ValueError):
        messages.error(request, "Invalid order total found. Please place the order again.")
        return redirect(checkout)

    amount = total_price * 100
    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_0ib0jPwwZ7I1lT")
    razorpay_key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "VjHNO5zKeKxz8PYe7VnzwxMR")

    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
    if customer.Razorpay_order_id and customer.Payment_status == "Pending":
        payment_order_id = customer.Razorpay_order_id
    else:
        payment_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        })
        payment_order_id = payment_order["id"]
        customer.Razorpay_order_id = payment_order_id
        customer.Payment_status = "Initiated"
        customer.save(update_fields=["Razorpay_order_id", "Payment_status"])

    context = {
        "categories": categories,
        "customer": customer,
        "display_amount": total_price,
        "amount": amount,
        "razorpay_key_id": razorpay_key_id,
        "payment_order_id": payment_order_id,
        "payment_success_url": reverse("payment_success"),
        "payment_failed_url": reverse("payment_failed"),
    }
    return render(request, "payment.html", context)


def payment_success(request):
    if request.method != "POST":
        messages.error(request, "Invalid payment response.")
        return redirect(payment_page)

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    order = OrderDb.objects.filter(Razorpay_order_id=razorpay_order_id).order_by("-id").first()
    if order is None:
        messages.error(request, "Order not found for this payment.")
        return redirect(checkout)

    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_0ib0jPwwZ7I1lT")
    razorpay_key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "VjHNO5zKeKxz8PYe7VnzwxMR")
    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })
    except razorpay.errors.SignatureVerificationError:
        order.Payment_status = "Failed"
        order.Razorpay_payment_id = razorpay_payment_id
        order.Razorpay_signature = razorpay_signature
        order.save(update_fields=["Payment_status", "Razorpay_payment_id", "Razorpay_signature"])
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect(payment_page)

    order.Payment_status = "Paid"
    order.Razorpay_payment_id = razorpay_payment_id
    order.Razorpay_signature = razorpay_signature
    order.save(update_fields=["Payment_status", "Razorpay_payment_id", "Razorpay_signature"])

    CartDb.objects.filter(Username=order.Username).delete()
    messages.success(request, "Payment successful. Your order has been confirmed.")
    return redirect(home_page)


def payment_failed(request):
    razorpay_order_id = request.GET.get("order_id")
    order = OrderDb.objects.filter(Razorpay_order_id=razorpay_order_id).order_by("-id").first()
    if order is not None and order.Payment_status != "Paid":
        order.Payment_status = "Failed"
        order.save(update_fields=["Payment_status"])

    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return redirect(payment_page)
