from django import forms
from .models import *
from world.models import Location

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
        labels = {
        "camps": "Campgrounds",
        }


class MoveCaravanForm(forms.ModelForm):

    class Meta:
        model = Caravan
        fields = ['currently_at']
        labels = {
        "currently_at": "Move To",
        }


class CreateMemberBase(forms.ModelForm):

    class Meta:
        model = MemberBase
        fields = '__all__'


class HireCrewForm(forms.ModelForm):

    class Meta:
        model = CrewMember
        fields = ['base', 'hired_by']


