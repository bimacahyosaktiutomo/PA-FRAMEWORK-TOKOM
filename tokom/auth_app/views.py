from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisForm

def register(request):
    if request.method == 'POST':
        form = UserRegisForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #login user habis regis
            messages.success(request, "Registration Successful!")
            return redirect('tokom:dashboard')
        else:
            messages.error(request, "Registration Failed. Invalid registration info, try again!")
    else:
        form = UserRegisForm()
    return render(request, 'auth_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Login Succeessful! Youre now logged in as {username}")
                return redirect('tokom:dashboard')
            else:
                messages.error(request, "Invalid Username or Password.")
        else:
            messages.error(request, "Invalid Username or Password.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth_app/login.html', {'form':form})
       
def user_logout(request):
    logout(request)
    messages.info(request, f"Logout Successful!")
    return redirect('tokom:home')