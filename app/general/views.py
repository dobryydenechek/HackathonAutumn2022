from urllib.robotparser import RequestRate
from xmlrpc.client import ResponseError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def main(request, *args, **kwargs):
    return render(request, 'start.html')


def sheet(request, *args, **kwargs):
    return render(request,'sheet.html')
    

def signin(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username and password:
            if User.objects.get(username=username):
                login(request, request.user)
                return redirect('sheet')
        messages.error(request, 'Username or password is incorrect')
        return render(request,'signin.html')
    else: raise ConnectionError
    

def signup(request, *args, **kwargs):
    return render(request,'signup.html')

def signout(request, *args, **kwargs):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')
    

def create_persone(request, *args, **kwargs):
    return render(request,'create_persone.html')
    