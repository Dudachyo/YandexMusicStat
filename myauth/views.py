from django.contrib.admindocs.views import user_has_model_view_permission
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm , TokenForm
from yandex_music import Client


def login_page_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'login':
            return login_view(request)
        elif action == 'register':
            return register_view(request)

    # GET запрос
    if request.user.is_authenticated:
        return redirect('profile-token')

    return render(request, 'myauth/Auth.html', {
        'form1': LoginForm(),
        'form2': RegisterForm()
    })


def profileToken_view(request):
    if request.method == "POST":
        print(request.POST)
        form = TokenForm(request.POST)
        if form.is_valid():
            try:
                Client(form.cleaned_data['token']).init()
            except:
                return render(request, 'myauth/profile-token.html', context={'form': form , 'error': True})
            user = request.user
            user.userprofile.save_token(form.cleaned_data['token'])
            return redirect('profile' , username=request.user.username)
        else:
            return render(request, 'myauth/profile-token.html', context={'form': form , 'error': True})

    if request.user.is_authenticated:
        if request.user.userprofile.has_token():
            return redirect('profile', username=request.user.username)
        form = TokenForm()
        return render(request, 'myauth/profile-token.html', {'form': form , 'user': request.user})
    else:
        return redirect('auth-page')

def profile_view(request , username):
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("Ops page not found")

    if request.user.username == username:
        if user.userprofile.has_token():
            token = user.userprofile.get_token()
            client = Client(token).init()
            liked_context = create_like_playlist(client, 5)

            return render(request, 'myauth/profile.html', context=liked_context | {'user': user})
        else:
            return redirect('profile-token')
    else:
        if user.userprofile.hidden:
            return HttpResponse("User is hidden")
        else:
            token = user.userprofile.get_token()
            client = Client(token).init()
            liked_context = create_like_playlist(client, 5)

            return render(request, 'myauth/profile.html', context=liked_context | {'user': user})

def redirect_to_profile_view(request):
    return redirect('profile', request.user.username)
def logout_view(request):
    logout(request)
    return redirect('main-page')

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
            return redirect('profile-token')
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
        return redirect('profile-token')

    return render(request, 'myauth/Auth.html', {
        'error': 'Error',
        'form1': LoginForm(),
        'form2': RegisterForm()
    })

def create_like_playlist(client, count):
    tracks = list(client.users_likes_tracks()[:count])
    liked_track_list = []
    for track_obj in tracks[:5]:  # Get first 5 liked tracks
        id = track_obj.id
        track = track_obj.fetch_track()
        title = track.title
        artist = " " + ', '.join(artist.name for artist in track.artists)
        url = "https://music.yandex.ru/track/" + str(id)

        img = None
        if track.cover_uri:
            img = f"https://{track.cover_uri.replace('%%', '200x200')}"

        liked_track_list.append({
            'liked_title': title,
            'liked_artist': artist,
            'liked_image': img,
            'liked_url': url
        })
    context = {"liked_track_list": liked_track_list}
    return context

def create_liked_artist(client, count):
    pass

def page_view(request):
    return render(request, 'myauth/profile-edit.html', {})


