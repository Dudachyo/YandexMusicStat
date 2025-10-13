from django.http import HttpResponse
from django.shortcuts import render , redirect
from yandex_music import Client

def main_page_view(request):

    saved_token = request.COOKIES.get('token')

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
            context = create_like_playlist(client)

            response = render(request, 'main/main-page.html', context=context)
            response.set_cookie('token', token , max_age=30*24*60*60)
            return response

        except:
            context = {"error": "Ошибка!!! Проверьте ТОКЕН"}
            return render(request, 'main/main-page.html', context=context)

    else:
        if saved_token:
            client = Client(saved_token).init()
            # Создаёт context для 5-ти любимых песен
            context = create_like_playlist(client)
            return render(request, 'main/main-page.html', context=context)

        return render(request, 'main/main-page.html')


def create_like_playlist(client):
    tracks = list(client.users_likes_tracks()[:5])
    track_list = []
    for track_obj in tracks[:5]:  # Get first 5 liked tracks
        id = track_obj.id
        track = track_obj.fetch_track()
        title = track.title
        artist = track.artists[0].name if track.artists else "Unknown Artist"
        url = "https://music.yandex.ru/track/" + str(id)

        img = None
        if track.cover_uri:
            img = f"https://{track.cover_uri.replace('%%', '200x200')}"

        track_list.append({
            'title': title,
            'artist': artist,
            'image': img,
            'id': id,
            'url': url
        })
    context = {"track_list": track_list}
    return context