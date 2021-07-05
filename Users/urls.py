from django.urls import path
from . import views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('login/', users_views.Login, name='login'),
    path('logout/', users_views.Logout, name='logout'),
    path('profile/', users_views.profile, name='profile'),
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name="password_reset_confirm"),
    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name="password_reset_done"),
    path('password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name="password_reset_complete"),
]
