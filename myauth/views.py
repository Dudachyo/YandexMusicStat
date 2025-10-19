from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm



def login_page_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'login':
            return login_view(request)
        elif action == 'register':
            return register_view(request)

    # GET запрос
    if request.user.is_authenticated:
        return redirect('login_success')

    return render(request, 'myauth/Auth.html', {
        'form1': LoginForm(),
        'form2': RegisterForm()
    })


def home(request):
    return HttpResponse('Hello, world. Yandex.ru !')


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('login_success')
    return render(request, 'myauth/Auth.html', {
        'error': 'Email or password is incorrect',
        'form1': LoginForm(),
        'form2': RegisterForm()
    })


def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'myauth/Auth.html', {
                'error': 'Username already exists',
                'form1': LoginForm(),
                'form2': RegisterForm()
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('login_success')

    return render(request, 'myauth/Auth.html', {
        'error': 'Error',
        'form1': LoginForm(),
        'form2': RegisterForm()
    })
