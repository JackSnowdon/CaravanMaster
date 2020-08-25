from django.urls import path
from .views import *

urlpatterns = [
    path('party_home/', party_home, name="party_home"),
    path('create_avatar/', create_avatar, name="create_avatar"),
    path(r'avatar_screen/<int:pk>', avatar_screen, name="avatar_screen"),
    path(r'delete_avatar/<int:pk>', delete_avatar, name="delete_avatar"),
]