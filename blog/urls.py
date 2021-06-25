from django.urls import path
from . import views as blog_views

urlpatterns = [
    path('', blog_views.home, name='home'),
    path('search/', blog_views.search, name="search"),
    path('category/<str:cat>/', blog_views.category, name="category"),
    path('post/<int:pk>/', blog_views.singlePost, name="single-post"),
]
