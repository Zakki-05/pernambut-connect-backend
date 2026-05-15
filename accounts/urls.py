from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    
    # Password Reset
    path('forgot-password/', views.CustomPasswordResetView.as_view(), name='forgot_password'),
    path('forgot-password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='reset_password'),
    path('reset-password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
