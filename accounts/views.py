from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from django.db.models import Q

User = get_user_model()

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user) # Don't login immediately if you prefer, or do
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Find user
            try:
                user_obj = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
                # Standard authenticate expects 'username' keyword even if it's an email
                user = authenticate(request, username=user_obj.email, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0) # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600) # 2 weeks
                
                messages.success(request, f'Welcome back, {user.name or user.username}!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required(login_url='accounts:login')
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        # Also initialize PasswordChangeForm
        password_form = PasswordChangeForm(request.user, request.POST)
        
        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) # Important, to keep the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # Initial data for fullname
        initial_data = {'fullname': request.user.name}
        form = CustomUserChangeForm(instance=request.user, initial=initial_data)
        password_form = PasswordChangeForm(request.user)
        
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'password_form': password_form
    })

# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
