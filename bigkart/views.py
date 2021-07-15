from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product

def index(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()
    context = {
        'products' :products,
        'product_count' : product_count,
    }
    return render(request, 'home.html', context)