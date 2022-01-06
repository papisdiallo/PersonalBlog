from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import Post, Category, Comment
from django.db.models import Count, Q
from Marketing.models import Subscriber
from .forms import CommentForm, ContactForm
from fonctions.funtions import counting_categories, get_context, process_post_request
from django.contrib import messages
from django.conf import settings
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.core.mail import EmailMessage
from Api.utils import Util


def home(request):
    context = get_context(request)
    form = context["form"]
    process_post_request(request, form)
    return render(request, "blog/index.html", context)


def category(request, cat):
    context = get_context(request)
    form = context["form"]
    process_post_request(request, form)
    context["posts"] = Post.objects.filter(category__name=cat).order_by("-date_posted")

    return render(request, "blog/category.html", context)


def singlePost(request, post_slug):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, post_slug=post_slug)
    comments = Comment.objects.all()
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
        return redirect("single-post/")
    context = get_context(request)
    context["post"] = post
    context["form"] = form
    context["comments"] = comments
    context["comment_count"] = post.comments.filter(
        author__is_developer_account=False
    ).count()
    return render(request, "blog/single.html", context)


def CommentView(request, pk):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    if request.is_ajax():
        if form.is_valid():
            content = request.POST.get("content")
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.content = content
            comment.save()
    context = {
        "comment": comment,
    }
    # the single_comment template is a partial template to be added after the post
    return render(request, "blog/single_comment.html", context)


def search(request):
    context = get_context(request)
    form = context["form"]
    process_post_request(request, form)
    q = request.GET.get("q")
    if q:
        queryset = Post.objects.filter(
            Q(title__icontains=q) | Q(overview__icontains=q) | Q(category__name=q)
        ).distinct()
    result_count = queryset.count()

    context["count"] = result_count
    context["q"] = q
    context["posts"] = queryset
    return render(request, "blog/search.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.is_ajax():
        response = dict()
        if form.is_valid():
            email_data = dict()
            email_data["subject"] = "Thanks For contacted me"
            email_data["to_email"] = form.cleaned_data.get("email", "")
            email_data[
                "email_body"
            ] = "Thank you for contacting me. We will be in touch as soon as possible!\n Please feel free to reply for any question or request.\n Best Regards!!\n Sahine"
            email_data["from_email"] = settings.EMAIL_HOST_USER
            Util.send_email(email_data)  # send the email to my self
            response["success"] = True
            return JsonResponse(response)
        else:
            response["success"] = False
            csrf_context = {}
            csrf_context.update(csrf(request))
            formErrors = render_crispy_form(form, context=csrf_context)
            response["formErrors"] = formErrors
            return JsonResponse(response)
    context = {
        "form": form,
    }
    return render(request, "blog/contact.html", context)


def about(request):
    context = get_context(request)
    return render(request, "blog/about.html", context)
