from django.urls import path
from .views import *

urlpatterns = [
    path('party_home/', party_home, name="party_home"),
    path('create_avatar/', create_avatar, name="create_avatar")
]