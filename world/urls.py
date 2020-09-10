from django.urls import path
from .views import *

urlpatterns = [
    path('world_index/', world_index, name="world_index"),
    path('create_location/', create_location, name="create_location"),
    path(r'edit_location/<int:pk>', edit_location, name="edit_location"),
    path(r'delete_location/<int:pk>', delete_location, name="delete_location"),
    path(r'location/<int:pk>', location, name="location"),
    path(r'create_camp/<int:pk>', create_camp, name="create_camp"),
    path(r'campground/<int:pk>', campground, name="campground"),
    path(r'hire_merc/<int:pk>/<int:locpk>', hire_merc, name="hire_merc"),
]