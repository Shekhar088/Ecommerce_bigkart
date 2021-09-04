from accounts.models import Account
from django.db import models
from django.db.models.deletion import CASCADE
from store.models import Product
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity * self.product.price


    def __unicode__(self):
        return self.product
