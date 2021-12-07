from django.core import paginator
from carts.models import CartItem
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, RatingReview
from category.models import Category
from carts.models import Cart,CartItem
from django.core.paginator import EmptyPage, Paginator,PageNotAnInteger
from .models import Product
from django.db.models import Q
from orders.models import OrderProduct

from .forms import ReviewForm
from django.contrib import messages
from carts.views import _cart_id

# Create your views here.
def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug !=None:
        categories = get_object_or_404(Category, slug= category_slug)
        products = Product.objects.filter(category=categories, is_available =True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available= True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context={
        
        'products':paged_products,
        'product_count':product_count,
    }
    return render(request, "store/store.html",context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug= category_slug, slug=product_slug)
        cart_item = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()

    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id = product.id)
        except OrderProduct.DoesnotExists():
            orderproduct = None
    else:
        orderproduct= None

    #Get review info
    reviews = RatingReview.objects.filter(product_id= product.id, status=True)
    context ={
        'product': product,
        'cart_item' : cart_item,
        'orderproduct' : orderproduct,
        'reviews'   :reviews,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    
    context={
        'products':products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
            reviews = RatingReview.objects.get(user__id=request.user.id, product__id= product_id)
            form = ReviewForm(request.POST, instance =reviews)
            form.save()
            messages.success(request,"Review has been updated")        
            return redirect(url)
        except RatingReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = RatingReview()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,"Thank You For the Review")
                return redirect(url)


