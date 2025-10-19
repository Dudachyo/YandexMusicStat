
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
    path('profile/', home, name='profile'),
]
