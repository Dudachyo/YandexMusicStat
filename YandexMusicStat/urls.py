
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.main_page_view , name='main-page'),
    path('login/' , include('myauth.urls')),
]
