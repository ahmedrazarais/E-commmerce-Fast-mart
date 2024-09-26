from django.shortcuts import render, get_object_or_404, redirect
from signup.models import Category, Product
from django.contrib import messages


# Decorator to check if user is authenticated
def session_required(view_func):
    def wrapper(request, *args, **kwargs):
        print("Session data:", request.session.items())
        if not request.session.get('is_authenticated'):
            messages.error(request, 'You need to login or register to access Fast-Mart.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper




def about_page(request):
    return render(request, "about.html")


# views to get all categories and display to homepage
def extract_cataegories_home_page(request):   
    cataegories = Category.objects.all()
    return render(request, "home.html", {"all_cataegories": cataegories})

# View to display products for a specific category
def category_products(request, category_id): 
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'all_products.html', {
        'category': category,
        'products': products
    })




@session_required
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # check if product is available
    if product.quantity <= 0:
        messages.error(request, 'This product is out of stock.Please check back later.')
        return redirect('home')
    return render(request, 'product_details.html', {
        'product': product
    })


def search_page(request):
    messages.error(request, 'Search functionality is not yet implemented.Working on It')
    return redirect('home')


