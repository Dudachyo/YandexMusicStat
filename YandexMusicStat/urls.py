
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path , include
from myauth.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('' , views.main_page_view , name='main-page'),
    path('admin/', admin.site.urls),
    path('login/' , include('myauth.urls')),
    path('logout/', logout_view, name='logout'),
    path('profile-token/', profileToken_view, name='profile-token'),
    path('profile/', redirect_to_profile_view),
    path('profile/user/<slug:username>/' , profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
