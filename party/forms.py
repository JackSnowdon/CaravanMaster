from django import forms
from .models import *

class AvatarForm(forms.ModelForm):
    
    class Meta:
        model = Avatar
        exclude = ['created_by', 'gold', 'xp', 'level']
        

class RenameAvatar(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ['name']


class CaravanForm(forms.ModelForm):

    class Meta:
        model = Caravan
        fields = '__all__'


class CreateMemberBase(forms.ModelForm):

    class Meta:
        model = MemberBase
        fields = '__all__'


class HireCrewForm(forms.ModelForm):

    class Meta:
        model = CrewMember
        fields = ['base', 'hired_by']

