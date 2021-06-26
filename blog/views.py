from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.db.models import Count, Q
from Marketing.models import Subscriber
from Marketing.forms import SubscriberForm
from .forms import CommentForm

from django.contrib import messages


def counting_categories():
    queryset = Post\
        .objects.values('category__name')\
        .annotate(Count('category'))
    return queryset


def get_context(request):
    posts = Post.objects.all().order_by('-date_posted')
    form = SubscriberForm(request.POST or None)
    categories = Category.objects.all()
    latest_posts = posts[:4]
    category_counting = counting_categories()
    context = {'posts': posts,
               'categories': categories,
               'latest_posts': latest_posts,
               'category_counting': counting_categories,
               'form': form,
               }
    return context


def process_post_request(request, form):
    if form.is_valid():
        form.save()
        messages.success(request, "Thank You for your subcription to the newsletter")
        return redirect('/')


def home(request):
    context = get_context(request)
    form = context['form']
    process_post_request(request, form)
    return render(request, 'blog/index.html', context)


def category(request, cat):
    context = get_context(request)
    form = context['form']
    process_post_request(request, form)
    context['posts'] = Post.objects.\
        filter(category__name=cat).\
        order_by('-date_posted')

    return render(request, 'blog/category.html', context)


def singlePost(request, pk):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.all()
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('/')
    context = get_context(request)
    context['post'] = post
    context['form'] = form
    context['comments'] = comments
    return render(request, 'blog/single.html', context)


def search(request):
    context = get_context(request)
    form = context['form']
    process_post_request(request, form)
    q = request.GET.get('q')
    if q:
        queryset = Post.objects.filter(
            Q(title__icontains=q) |
            Q(overview__icontains=q)).distinct()
    result_count = queryset.count()

    context['count'] = result_count
    context['q'] = q
    context['posts'] = queryset
    return render(request, 'blog/search.html', context)
