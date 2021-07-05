from django.shortcuts import render, redirect
from .forms import (
    UserRegistrationForm, 
    LoginForm, UserUpdateForm,
    UserProfileForm
)
from fonctions.funtions import get_context
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  


def register(request):
    form1 = UserRegistrationForm(request.POST or None)
    if form1.is_valid():
        form1.save()
        username = form1.cleaned_data.get('username')
        password = form1.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, f"Hi, {username}! Your account have been created, Complete your profile")
        return redirect('home')
    context = get_context(request)
    context['form1'] = form1
    return render(request, 'users/register.html', context)


def Login(request):
    form1 = LoginForm(request.POST or None)
    if form1.is_valid():
        username = form1.cleaned_data.get('Username_or_Email')
        password = form1.cleaned_data.get('Password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    context = get_context(request)
    context['form1'] = form1
    return render(request, 'users/login.html', context)


def Logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully !')
    return render(request, 'blog/index.html')


def profile(request):
    user = request.user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has beed updated successfully")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = UserProfileForm(instance=user.profile)
    context = {
        'user': user,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
