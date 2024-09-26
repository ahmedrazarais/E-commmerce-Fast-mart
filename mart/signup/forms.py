from django import forms
from django.core.mail import send_mail
from django.conf import settings  # Import settings
from .models import Accounts_Table, Cart, History
import random
import string
import re


class Register_Form(forms.ModelForm):
    security = forms.CharField(
        label="What is your favorite pet animal?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )

    verification_code = forms.CharField(
        label="Verification Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter code sent to your email'}),
        required=False
    )

    class Meta:
        model = Accounts_Table
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'security', 'address', 'verification_code')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))

    def send_verification_email(self, email, code):
        subject = 'Your Verification Code'
        message = f'Your verification code is {code}. Please enter it to complete your registration.'
        from_email = settings.EMAIL_HOST_USER  # Use the configured email address
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('verification_code')
        user_email = cleaned_data.get('email')

        stored_code = self.request.session.get('verification_code')

        if self.request.method == "POST":
            if not stored_code:
                # Send verification code only if it's not already sent
                verification_code = self.generate_verification_code()
                self.request.session['verification_code'] = verification_code
                self.send_verification_email(user_email, verification_code)
                self.add_error('verification_code', 'Please enter the verification code sent to your email.')
            elif code and code != stored_code:
                self.add_error('verification_code', 'Incorrect verification code.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.request.session.pop('verification_code', None)
            # Cart.objects.create(user=user)
            # History.objects.create(user=user)
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if Accounts_Table.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Accounts_Table.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email
