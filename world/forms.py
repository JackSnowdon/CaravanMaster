from django import forms
from .models import *

class LocationForm(forms.ModelForm):
    
    class Meta:
        model = Location
        fields = '__all__'


class CampgroundForm(forms.ModelForm):

    class Meta:
        model = Campground
        fields = ['gold']


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = '__all__'