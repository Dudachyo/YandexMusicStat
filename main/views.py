from django.http import HttpResponse
from django.shortcuts import render , redirect
from yandex_music import Client
from django.contrib.auth.models import User
def main_page_view(request):

    if request.user.is_authenticated:
        pass
    if request.method == "POST":
        try:
            # Получаем токен от пользователя
            token = request.POST.get('token', '').strip()

            # Если Токен не обнаружен -> Возв. стр с ошибкой
            if not token:
                context = {"error": "Введите ТОКЕН"}
                return render(request, 'main/main-page.html', context=context)

            # Инициальзация пользователя
            client = Client(token).init()
            # Создаёт context для 5-ти любимых песен
            # liked_context = create_like_playlist(client , 5)
            # Создаёт context для 5-ти песен в чарте
            chart_context = create_chart_playlist(client, 5)

            context = chart_context

            response = render(request, 'main/main-page.html', context=context)
            response.set_cookie('token', token , max_age=30*24*60*60)
            return response

        except:
            context = {"error": "Error!!! invalid token"}
            return render(request, 'main/main-page.html', context=context)

    else:
        # if token:
        #     client = Client(request.user.last_name).init()
        #     # Создаёт context для 5-ти любимых песен
        #     # liked_context = create_like_playlist(client, 5)
        #     # Создаёт context для 5-ти песен в чарте
        #     chart_context = create_chart_playlist(client, 5)
        #
        #     context = chart_context
        #     return render(request, 'main/main-page.html', context=context)

        return render(request, 'main/main-page.html')


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

def create_chart_playlist(client, count):
    CHART_ID = 'world'
    tracks = client.chart(CHART_ID).chart.tracks[:count]
    chart_track_list = []
    for track_short in tracks[:5]:  # Get first 5 chart tracks
        track, chart = track_short.track, track_short.chart
        id = track.id
        title = track.title
        artist = " " + ', '.join(artist.name for artist in track.artists)
        url = "https://music.yandex.ru/track/" + str(id)

        img = None
        if track.cover_uri:
            img = f"https://{track.cover_uri.replace('%%', '200x200')}"
        chart_track_list.append({
            'chart_title': title,
            'chart_artist': artist,
            'chart_image': img,
            'chart_url': url
        })
    context = {"chart_track_list": chart_track_list}
    return context
