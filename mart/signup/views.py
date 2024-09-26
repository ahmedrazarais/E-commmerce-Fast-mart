from django.shortcuts import render, redirect
from .forms import Register_Form
from django.contrib import messages
from django.http import JsonResponse

def registration_home(request):
    return render(request, "signup/signup_home.html")



def registration_form(request):
    if request.method == "POST":
        form = Register_Form(request.POST, request=request)  # Pass request to form

        if 'send_code' in request.POST:  # Handle AJAX request to send verification code
            email = request.POST.get('email')
            if email:
                verification_code = form.generate_verification_code()
                request.session['verification_code'] = verification_code
                form.send_verification_email(email, verification_code)
                return JsonResponse({'status': 'success', 'message': 'Verification code sent.'})
            return JsonResponse({'status': 'error', 'message': 'Email is required.'})

        if form.is_valid():
            # Check if verification code is correct
            code = form.cleaned_data.get('verification_code')
            stored_code = request.session.get('verification_code')

            if code and code == stored_code:
                user = form.save()  # Save the user only if verification code is correct

                # Automatically log the user in by creating a session
                request.session['username'] = user.username
                request.session['user_id'] = user.id
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.email
                request.session['security'] = user.security
                request.session['is_authenticated'] = True

                messages.success(request, 'You have successfully created your account in Fast-Mart.')
                return redirect("home")
            else:
                form.add_error('verification_code', 'Incorrect verification code.')
    else:
        form = Register_Form(request=request)  # Initialize form with request for GET requests

    return render(request, "signup/signup_form.html", {"registration_form": form})
