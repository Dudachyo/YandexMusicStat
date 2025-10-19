
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page_view,  name='auth-page'),
]
