from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


# Create your views here.

def party_home(request):
    profile = request.user.profile
    avas = Avatar.objects.filter(created_by=profile).order_by('name')[:5]
    return render(request, "party_home.html", {"avas": avas})


# Avatar

@login_required
def create_avatar(request):
    if request.method == "POST":
        ava_form = AvatarForm(request.POST)
        if ava_form.is_valid():
            form = ava_form.save(commit=False)
            form.created_by = request.user.profile
            form.save()
            messages.error(request, "Created {0}".format(form.name), extra_tags="alert")
            return redirect("party_home")    
    else:
        ava_form = AvatarForm()
    return render(request, "create_avatar.html", {"ava_form": ava_form})

