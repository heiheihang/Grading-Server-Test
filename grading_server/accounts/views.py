from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.forms import LoginForm, RegisterForm
from .token import account_activation_token

from time import sleep

# Create your views here.


def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if 'next' in request.POST:
            next_url = request.POST['next']
        else:
            next_url = '/'
        args = {'form': form, 'next': next_url}
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            args.update(
                {'message': 'Error: username and password does not match'})
        # TODO: timeout should be account-bound, instead of instance-bound
        sleep(3.0)
        return render(request, 'accounts/login.html', args)
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
            user = User.objects.create_user(
                form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            current_site = get_current_site(request)
            email_content = render_to_string('accounts/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user('Activate Account', email_content)
            messages.success(request, ('You have been registered! Please verify the your email address.'))
            return redirect('/')
    return render(request, 'accounts/register.html', {'form': form})

def verify_email_view(request, uidb64, token):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if not user is None and account_activation_token.check_token(user, token):
        user.email_verify.email_confirmed = True
        user.email_verify.save()
        messages.success(request, ('Your email have been verified.'))
    else:
        # TODO: resend verify email option somewhere?
        messages.warning('Invalid email verify link.')
    return redirect('/')

# TODO: password reset via email
