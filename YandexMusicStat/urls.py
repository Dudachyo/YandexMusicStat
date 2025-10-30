
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path , include
from myauth.views import *

urlpatterns = [
    path('' , views.main_page_view , name='main-page'),
    path('admin/', admin.site.urls),
    path('login/' , include('myauth.urls')),
    path('logout/', logout_view, name='logout'),
    path('profile-token/', profileToken_view, name='profile-token'),
    path('profile/', redirect_to_profile_view),
    path('profile/user/<slug:username>/' , profile_view, name='profile'),
    path('profile/edit/', page_view, name='profile-edit'),
]
