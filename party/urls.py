from django.urls import path
from .views import *

urlpatterns = [
    path('party_home/', party_home, name="party_home"),
    path('create_avatar/', create_avatar, name="create_avatar"),
    path(r'avatar_screen/<int:pk>', avatar_screen, name="avatar_screen"),
    path(r'delete_avatar/<int:pk>', delete_avatar, name="delete_avatar"),
    path(r'rename_avatar/<int:pk>', rename_avatar, name="rename_avatar"),
    path(r'start_caravan/<int:pk>', start_caravan, name="start_caravan"),
    path(r'caravan/<int:pk>', caravan, name="caravan"),
    path(r'assign_crew_to_caravan/<int:crewpk>/<int:cavpk>', assign_crew_to_caravan, name="assign_crew_to_caravan"),
    path(r'member_home/', member_home, name="member_home"),
    path(r'create_member_base/', create_member_base, name="create_member_base"),
    path(r'delete_member_base/<int:pk>', delete_member_base, name="delete_member_base"),
    path(r'member_base/<int:pk>', member_base, name="member_base"),
    path(r'crew/<int:pk>', crew, name="crew"),
    path(r'hire_crew/<int:crewpk>/<int:avapk>', hire_crew, name="hire_crew"),
    path(r'fire_crew/<int:crewpk>/<int:avapk>', fire_crew, name="fire_crew"),
    path(r'crew_member/<int:pk>', crew_member, name="crew_member"),
]