from django.shortcuts import render, get_object_or_404, redirect
from signup.models import Product, Cart, Accounts_Table
from django.contrib import messages
from django.db import transaction

def add_to_cart(request, product_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        
        if not user_id:
            messages.error(request, 'You need to log in to add items to your cart.')
            return redirect('login')
        
        user = get_object_or_404(Accounts_Table, id=user_id)
        product = get_object_or_404(Product, id=product_id)
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.quantity:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', product_id=product_id)
        
        with transaction.atomic():
            # Reduce the quantity of the product
            product.quantity -= quantity
            product.save()
            
            # Add to cart
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                product_id=product.id,
                defaults={
                    'product_name': product.name,
                    'product_quantity': quantity,
                    'price_per_unit': product.price,
                 
                    
                   
                }
            )
            
            if not created:
                cart_item.product_quantity += quantity
                cart_item.save()
        
        messages.success(request, 'Product added to cart successfully.')
        
         # redirect to that cataegory
        return redirect('category_products', category_id=product.category.id)


def increase_quantity(request, product_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(Accounts_Table, id=user_id)
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.filter(user=user, product=product).first()

        if cart_item:
            # check that product quantity is less than the available quantity
            if cart_item.product_quantity > product.quantity:
                messages.error(request, 'Not enough stock available.')
                return redirect('cart_home')
            cart_item.product_quantity += 1
            cart_item.save()

            product.quantity -= 1
            product.save()

            messages.success(request, 'Product quantity increased successfully.')
        else:
            messages.error(request, 'Product not found in cart.')
    else:
        messages.error(request, 'You need to log in to modify your cart.')

    return redirect('cart_home')

def decrease_quantity(request, product_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(Accounts_Table, id=user_id)
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.filter(user=user, product=product).first()

        if cart_item:
            if cart_item.product_quantity > 1:
                cart_item.product_quantity -= 1
                cart_item.save()

                product.quantity += 1
                product.save()

                messages.success(request, 'Product quantity decreased successfully.')
            else:
                cart_item.delete()
                product.quantity += cart_item.product_quantity
                product.save()

                messages.success(request, 'Product removed from cart successfully.')
        else:
            messages.error(request, 'Product not found in cart.')
    else:
        messages.error(request, 'You need to log in to modify your cart.')

    return redirect('cart_home')


def clear_cart(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(Accounts_Table, id=user_id)
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            try:
                product = Product.objects.get(id=item.product_id)
                product.quantity += item.product_quantity
                product.save()
            except Product.DoesNotExist:
                messages.error(request, f'Product with ID {item.product_id} does not exist.')
                continue
        cart_items.delete()
        messages.success(request, 'Cart cleared successfully.')
    else:
        messages.error(request, 'You need to log in to modify your cart.')
    return redirect('cart_home')

def cart_home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_instance = get_object_or_404(Accounts_Table, id=user_id)
        cart_items = Cart.objects.filter(user=user_instance)
        
        # Calculate the total price for each item
        for item in cart_items:
            item.total_price = item.product_quantity * item.price_per_unit

        # Pass the total value to the context
        total_cart_value = sum(item.total_price for item in cart_items)
        
        return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_cart_value': total_cart_value})
    
    messages.error(request, 'You need to register or log in to view your cart.')
    return redirect('home')  # Redirect to home if user is not logged in
