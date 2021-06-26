from django.urls import path
from . import views as users_views


urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('login/', users_views.Login, name='login'),
    path('logout/', users_views.Logout, name='logout'),
]
