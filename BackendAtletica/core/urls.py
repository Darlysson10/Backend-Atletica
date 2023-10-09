from django.urls import path
from .views import register, login, logout, enviar_email

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('enviaremail/', enviar_email),
]
