from django.db import models

# Create your models here.

class User_RegistrationDb(models.Model):
    Username = models.CharField(max_length=50,null=True,blank=True)
    Password = models.CharField(max_length=50,null=True,blank=True)
    Confirm_Password = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)

class ContactDb(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=100,blank=True,null=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Message = models.TextField(null=True,blank=True)
    Subject = models.TextField(null=True,blank=True)


class CartDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Total_price = models.IntegerField(null=True,blank=True)
    Product_name = models.CharField(max_length=100,null=True,blank=True)

class OrderDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    Full_name = models.CharField(max_length=100,null=True,blank=True)
    Place = models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Address = models.CharField(max_length=200,null=True,blank=True)
    Pincode = models.IntegerField(null=True,blank=True)
    Message = models.TextField(null=True,blank=True)
    Mobile = models.BigIntegerField(null=True,blank=True)
    Total_price =models.CharField(max_length=100,null=True,blank=True)
    Razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    Razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    Razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    Payment_status = models.CharField(max_length=30, null=True, blank=True, default="Pending")

