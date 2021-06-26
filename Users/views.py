from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def authenticationProcess(request, form, username, password):
    pass    


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
    context = {
        'form1': form1,
    }
    return render(request, 'users/register.html', context)


def Login(request):
    form1 = LoginForm(request.POST or None)
    if form1.is_valid():
        username = form1.cleaned_data.get('Username_or_Password')
        password = form1.cleaned_data.get('Password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    context = {'form1': form1}
    return render(request, 'users/login.html', context)

def Logout(request):
    logout(request)
    return render(request, 'users/logout.html')
