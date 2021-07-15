from django.db import models
from django.db.models.deletion import CASCADE
from category.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)


    def __str__(self):
        return self.product_name