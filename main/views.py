from django.shortcuts import render
from yandex_music import Client

def main_page_view(request):
    if request.method == "POST":
        try:
            token = request.POST.get('token', '').strip()
            if not token:
                context = {"error": "Введите ТОКЕН"}
                return render(request, 'main/main-page.html', context=context)

            client = Client(token).init()
            tracks = client.users_likes_tracks()

            track_list = []
            for track_obj in tracks[:5]:  # Get first 5 liked tracks
                track = track_obj.fetch_track()
                title = track.title
                artist = track.artists[0].name if track.artists else "Unknown Artist"

                img = None
                if track.cover_uri:
                    img = f"https://{track.cover_uri.replace('%%', '200x200')}"

                track_list.append({
                    'title': title,
                    'artist': artist,
                    'image': img
                })

            context = {"track_list": track_list}
            return render(request, 'main/main-page.html', context=context)

        except:
            context = {"error": "Ошибка!!! Проверьте ТОКЕН"}
            return render(request, 'main/main-page.html', context=context)

    else:
        return render(request, 'main/main-page.html')