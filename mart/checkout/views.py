from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from signup.models import Cart, History,Accounts_Table  

# Render the checkout page if the user is authenticated
def checkout_page(request):
    if request.session.get('is_authenticated'):  # Or use request.user.is_authenticated
        return render(request, "checkout/checkout_home.html")
    else:
        messages.error(request, 'You need to login or register to access Fast-Mart.')
        return redirect('login')  # Redirect to login page if user is not authenticated



def checkout_other(request):
    return render(request, "checkout/other_methods_checkout.html")




# Import your Cart and History models

def checkout_success(request):
    # Get the user's email from the session or user model
    user_email = request.session.get('email') or request.user.email
    
    # Get the user's cart items (adjusting the filter as per your Cart model)
    username = request.session.get('username')  # Assuming you store username in the session
    user = Accounts_Table.objects.get(username=username)  # Fetch the user instance
    user_cart = Cart.objects.filter(user=user)  # Fetch user's cart items
    
    if not user_cart.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')  # Redirect to cart page if empty

    # Format the cart items to include in the email
    cart_details = ""
    total_bill = 0
    for item in user_cart:
        cart_details += f"Product: {item.product_name}, Quantity: {item.product_quantity}, Price per unit: {item.price_per_unit}\n"
        total_bill += item.total_bill  # Using total_bill from the Cart model

    cart_details += f"\nTotal Bill: ${total_bill:.2f}"

    # Send the email with the cart details
    send_mail(
        'Your Fast-Mart Order',
        f'Thank you for shopping with Fast-Mart!\n\nYour order details:\n{cart_details}',
        settings.DEFAULT_FROM_EMAIL,  # The sender's email (configured in settings.py)
        [user_email],  # The recipient's email
        fail_silently=False,
    )
    
    # Create a history record for each cart item
    for item in user_cart:
        History.objects.create(
            user=user,
            product=item.product,  # Use the actual product instance
            product_name=item.product_name,
            product_quantity=item.product_quantity,
            price_per_unit=item.price_per_unit,
            total_bill=item.total_bill,
        )

    # Clear the cart after sending the email
    user_cart.delete()

    # Optionally add a success message
    messages.success(request, "Your order was placed successfully, and an email has been sent!")

    # Render the success page
    return render(request, "checkout/checkout_success.html")
