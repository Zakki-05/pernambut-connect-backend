from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    fullname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'file-input'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'fullname', 'profile_image')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not password:
            return password
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&#]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['fullname']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None # We handle password change separately
    fullname = forms.CharField(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'profile_image', 'phone_number', 'area')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['fullname']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )
    remember_me = forms.BooleanField(required=False, initial=False)
