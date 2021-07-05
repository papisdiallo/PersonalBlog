from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post, Category, Comment
from django.db.models import Count, Q
from Marketing.models import Subscriber
from .forms import CommentForm
from fonctions.funtions import counting_categories, get_context, process_post_request
from django.contrib import messages



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
        form.instance.post = post
        form.save()
        return redirect('single-post/')
    context = get_context(request)
    context['post'] = post
    context['form'] = form
    context['comments'] = comments
    return render(request, 'blog/single.html', context)

def CommentView(request, pk):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    if request.is_ajax():
        if form.is_valid():
            content = request.POST.get('content')
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.content = content
            instance.save()

    return JsonResponse({'content': content,})


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
