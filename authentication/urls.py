from django.contrib import admin
from django.urls import path, include
from .views import user_creation_view, user_signin_view

urlpatterns = [
    path('signup/', user_creation_view),
    path('signin/', user_signin_view),
]
