
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page_view , name='login'),
    path('login/', home, name='login_success'),
    path('logout/', logout_view, name='logout_success'),
]
