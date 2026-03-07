from django.db import models

# Create your models here.

class CategoryDb(models.Model):
    Category_name = models.CharField(max_length=50,null=True,blank=True)
    Description = models.TextField(max_length=500,null=True,blank=True)
    Category_img = models.ImageField(upload_to="Category Images",blank=True,null=True)

class ProductDb(models.Model):
    CategoryName = models.CharField(max_length=100,null=True,blank=True)
    Product_Name = models.CharField(max_length=100,null=True,blank=True)
    Brand = models.CharField(max_length=100,null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Short_Description = models.TextField(null=True,blank=True)
    Detailed_Description = models.TextField(null=True,blank=True)
    Product_img1 = models.ImageField(upload_to="Product Images",null=True,blank=True)
    Product_img2 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    Product_img3 = models.ImageField(upload_to="Product Images", null=True, blank=True)