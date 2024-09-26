from django import forms
from django.core.exceptions import ValidationError

# Form for login-process
class Login_Form(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


# Custom password validator
def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least one number.')
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in value):
        raise ValidationError('Password must contain at least one special character.')


# Form for Forgot Password scenario
class Forgot_password(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    security = forms.CharField(
        max_length=50,
        required=True,
        label='What is your favorite pet animal?',
        help_text=''
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        validators=[validate_password]
    )
