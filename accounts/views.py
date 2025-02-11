from django.shortcuts import render, redirect
from .forms import UserCreateForm, AdminLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import AdminUser
from django.views.decorators.cache import cache_control  # For caching control


# ✅ Normal User Signup (Django Authentication)
def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreateForm()})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signupaccount.html', {
                    'form': UserCreateForm(),
                    'error': 'Username already taken. Choose a new username.'
                })
        else:
            return render(request, 'signupaccount.html', {
                'form': UserCreateForm(),
                'error': 'Passwords do not match'
            })


# ✅ Normal User Login (Django Authentication)
@never_cache
def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})
    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'Username and password do not match'
            })
        else:
            login(request, user)
            return redirect('home')


# ✅ Normal User Logout
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Prevent caching of the logout page
def logoutaccount(request):
    logout(request)
    return redirect('home')



