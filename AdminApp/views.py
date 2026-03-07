from django.contrib import  messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from AdminApp.models import CategoryDb, ProductDb
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from WebApp.models import ContactDb


# Create your views here.
def dashboard(request):
    categories=CategoryDb.objects.count()
    products=ProductDb.objects.count()
    return render(request,"dashboard.html",{"categories":categories,"products":products})

def add_category(request):
    return render(request,"add_category.html")

def save_category(request):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("desc")
        cat_img = request.FILES['img']
        obj = CategoryDb(Category_name=cat_name,Description=cat_desc,Category_img=cat_img)
        obj.save()
        messages.success(request,"category added successfully")
        return redirect(add_category)

def display_category(request):
    category = CategoryDb.objects.all()
    return render(request,"display_category.html",{"category":category})

def edit_category(request,cat_id):
    category = CategoryDb.objects.get(id=cat_id)
    return render(request,"edit_category.html",{"category":category})

def update_category(request,category_id):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("desc")
        try:
            img = request.FILES['Category_img']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = CategoryDb.objects.get(id=category_id).Category_img
        CategoryDb.objects.filter(id=category_id).update(Category_name=cat_name,Description=cat_desc,Category_img=file)
        messages.success(request,"category details updated")
        return redirect(display_category)

def delete_category(request,cat_id):
    data = CategoryDb.objects.filter(id=cat_id)
    data.delete()
    messages.error(request,"category deleted successfully")
    return redirect(display_category)
#****************************************************************************************************
def add_product(request):
    categories = CategoryDb.objects.all()
    return render(request,"add_product.html",{"categories":categories})

def save_product(request):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        pro_name = request.POST.get("pname")
        brand = request.POST.get("brand")
        shrt_desc = request.POST.get("sdesc")
        detailed_desc = request.POST.get("detailed_desc")
        pro_img1 = request.FILES['img1']
        pro_img2 = request.FILES['img2']
        pro_img3 = request.FILES['img3']
        price = request.POST.get("price")
        obj = ProductDb(CategoryName=cat_name,Product_Name=pro_name,
                        Brand=brand,Short_Description=shrt_desc,Detailed_Description=detailed_desc,
                        Product_img1=pro_img1,Product_img2=pro_img2,Product_img3=pro_img3,Price=price)
        obj.save()
        messages.success(request,"product added successfully")
        return redirect(add_product)

def display_product(request):
    product = ProductDb.objects.all()
    return render(request,"display_product.html",{"product":product})

def edit_product(request,pro_id):
    categories = CategoryDb.objects.all()
    product =ProductDb.objects.get(id=pro_id)
    return render(request,"edit_product.html",{"product":product,"categories":categories})

def update_product(request,product_id):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        pro_name = request.POST.get("pname")
        brand = request.POST.get("brand")
        shrt_desc = request.POST.get("sdesc")
        detailed_desc = request.POST.get("detailed_desc")
        try:
            img = request.FILES['Product_img1']
            fs = FileSystemStorage()
            file1 = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file1 = ProductDb.objects.get(id=product_id).Product_img1
        try:
            img = request.FILES['Product_img2']
            fs = FileSystemStorage()
            file2 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file2 = ProductDb.objects.get(id=product_id).Product_img2
        try:
            img = request.FILES['Product_img3']
            fs = FileSystemStorage()
            file3 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file3 = ProductDb.objects.get(id=product_id).Product_img3
        ProductDb.objects.filter(id=product_id).update(CategoryName=cat_name,
                    Product_Name=pro_name,Brand=brand,Short_Description=shrt_desc,Detailed_Description=detailed_desc,Product_img1=file1,
                    Product_img2=file2,Product_img3=file3)
        messages.success(request,"product details updated")
        return redirect(display_product)

def delete_product(request,pro_id):
    data = ProductDb.objects.filter(id=pro_id)
    data.delete()
    messages.success(request,"product deleted successfully")
    return redirect(display_product)

#************************************************************************************************

def admin_login_page(request):
    return render(request,"Admin_loginPage.html")

def admin_login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pswrd = request.POST.get('password')
        if User.objects.filter(username__contains=uname).exists():
            data=authenticate(username=uname, password=pswrd)
            if data is not None:
                login(request, data)
                request.session['username'] = uname
                request.session['password'] = pswrd
                messages.success(request,"Welcome to ElectroMart Dashboard")
                return redirect(dashboard)
            else:
                messages.error(request,"Invalid password")
                return redirect(admin_login_page)
        else:
            messages.error(request,"username does not exist")
            return redirect(admin_login_page)

def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login_page)

#**********************************************************************************************

def contact_details(request):
    contacts = ContactDb.objects.all()
    return render(request,"contact_details.html",{"contacts":contacts})

def delete_contact(request,con_id):
    data = ContactDb.objects.filter(id=con_id)
    data.delete()
    return redirect(contact_details)