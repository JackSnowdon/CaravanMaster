from django.urls import path
from .views import *

urlpatterns = [
    path('party_home/', party_home, name="party_home"),
]