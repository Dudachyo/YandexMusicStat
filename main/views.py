from django.http import HttpResponse
from django.shortcuts import render , redirect
from yandex_music import Client
from django.contrib.auth.models import User
def main_page_view(request):
        if request.user.is_authenticated:
            client = Client(request.user.userprofile.get_token()).init()
            chart_context = create_chart_playlist(client, 5)

            context = chart_context
            return render(request, 'main/main-page.html', context=context)
        else:
            return render(request, 'main/main-page.html')


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
