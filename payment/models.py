from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from store.models import Product
# Create your models here.

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length= 300)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300,blank=True , null=True)
    city = models.CharField(max_length=155)
    zip_code =models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="shipping_address" , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.full_name}-{self.city}"
    

class Order(models.Model):
    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=8 , decimal_places=2 , validators=[MinValueValidator(0)])

    date_ordered = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User,  on_delete=models.SET_NULL , related_name="orders",blank=True,null=True)
    
    def __str__(self):
        return f"Order-#{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , null=True)
    product = models.ForeignKey(Product ,on_delete=models.SET_NULL , null=True)
    product_name = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default =1)

    price = models.DecimalField(decimal_places=2 , max_digits=8 , validators=[MinValueValidator(0)])
    total_price  = models.DecimalField(decimal_places=2 , max_digits=12 , validators=[MinValueValidator(0)] , null=True)

    def __str__(self):
        return f"Order Item-{self.product}-#{self.id}"