from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250 , db_index = True)
    slug = models.SlugField(max_length=250 , unique=True)

    class Meta:
        verbose_name = "products"
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250 , default="un-branded")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0 , validators=[MinValueValidator(0)])
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    image = models.ImageField(upload_to = "products/")
    class Meta:
            verbose_name = "categories"
    def __str__(self):
        return self.title

    