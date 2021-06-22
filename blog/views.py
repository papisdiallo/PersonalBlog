from django.shortcuts import render
from .models import Post, Category


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    categories = Category.objects.all()
    latest_posts = posts[:3]
    context = {
        'posts': posts,
        'categories': categories,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/index.html', context)
