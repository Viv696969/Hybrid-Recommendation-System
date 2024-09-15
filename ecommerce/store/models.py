from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=250,blank=False,null=False,unique=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=300,null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    image=models.FileField(upload_to="product_images/",null=True,blank=True)
    image_url=models.CharField(max_length=800,blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)

    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField(blank=True,null=True)

    def __str__(self) -> str:
        return self.order.user.username
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField(blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username