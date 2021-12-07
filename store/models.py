from django.db import models
from django.db.models.deletion import CASCADE
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg,Count
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

    def get_url(self):
        return reverse('product_detail', args =[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name

    def AverageReview(self):
        reviews = RatingReview.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def CountReview(self):
        reviews = RatingReview.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count



class RatingReview(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    user    = models.ForeignKey(Account, on_delete=CASCADE)
    rating  = models.FloatField()
    review  = models.TextField(max_length=200, blank=True)
    subject = models.CharField(max_length=100,blank=True)
    ip      = models.CharField(max_length=100,blank=True)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject