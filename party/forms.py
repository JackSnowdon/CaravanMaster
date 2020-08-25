from django import forms
from .models import *

class AvatarForm(forms.ModelForm):
    
    class Meta:
        model = Avatar
        exclude = ['created_by', 'gold', 'xp', 'level']

