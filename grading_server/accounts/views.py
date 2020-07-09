from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.contrib.auth.models import User

from accounts.forms import LoginForm, RegisterForm

from time import sleep

# Create your views here.


def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if 'next' in request.POST:
            next_url = request.POST['next']
        else:
            next_url = '/'
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
        # TODO: timeout should be account-bound, instead of instance-bound
        sleep(3.0)
        return render(request, 'accounts/login.html', {'form': form, 'next': next_url})
    if request.method == 'GET':
        if 'next' in request.GET:
            next_url = request.GET['next']
        else:
            next_url = '/'
        return render(request, "accounts/login.html", {'form': form, 'next': next_url})
    return HttpResponseNotAllowed(['GET', 'POST'])


def custom_logout(request):
    # TODO: maybe POST instead of GET?
    if request.method == 'GET':
        logout(request)
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('/')
    return HttpResponseNotAllowed(['GET'])


def custom_register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            User.objects.create_user(
                request.POST['username'], email=request.POST['email'], password=request.POST['password'])
            # TODO: actually make a verify email thing
            return render(request, '/', {'message': 'You have been registered! Please verify the your email address.'})
    return render(request, 'accounts/register.html', {'form': form})

# TODO: password reset via email
