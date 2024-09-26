from django.shortcuts import render, redirect
from django.contrib import messages
from signup.models import Accounts_Table
from django.contrib.auth.hashers import make_password, check_password
from .forms import Login_Form, Forgot_password
from django.contrib.auth import login as auth_login




# Create your views here.
def login_home_page(request):
    return render(request, "signin/signin_home.html")

# Handle Login-Form View
def login_form_page(request):
    if request.method == "POST":
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username").strip()
            password = form.cleaned_data.get("password")

            # Check if the user exists in Accounts_Table
            user = Accounts_Table.objects.filter(username__iexact=username).first()

            if user is None:
                messages.error(request, 'The username you entered does not exist.')
            elif not check_password(password, user.password):
                messages.error(request, 'The password you entered is incorrect.')
            else:
                # Create a session for the user
                request.session['username'] = username
                request.session['user_id'] = user.id
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.email
                request.session['security'] = user.security
                request.session['is_authenticated'] = True
                messages.success(request, 'You have been logged in successfully.')
                
                
                
                return redirect('home')

    else:
        form = Login_Form()

    return render(request, "signin/signin_form.html", {"form": form})




def forgot_pswd(request):
    if request.method == "POST":
        form = Forgot_password(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username").strip()
            security = form.cleaned_data.get("security").strip()
            new_password = form.cleaned_data.get("new_password")

            # Check if the user exists in Accounts_Table
            user = Accounts_Table.objects.filter(username__iexact=username).first()

            if user is None:
                messages.error(request, 'The username you entered does not exist.')
            elif user.security != security:  # Direct comparison if security answer is not hashed
                messages.error(request, 'The security answer you entered is incorrect.')
            else:
                # Update the password
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')

                return redirect('home') 
            
    else:
        form = Forgot_password()

    return render(request, "signin/forgot_password.html", {"form": form})



def logout_view(request):
    messages.success(request, 'You have been logged out successfully.')
    request.session.flush()  # Clears all session data
    return redirect('home')  # Redirect to login page after logout