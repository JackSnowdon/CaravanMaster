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
            point_total = form.attack + form.defense + form.intel
            if point_total > 10:
                messages.error(request, "Overall Skills Above 10 ({0})".format(point_total), extra_tags="alert")
            elif point_total < 10:
                messages.error(request, "Overall Skills Below 10 ({0})".format(point_total), extra_tags="alert")
            else:
                form.save()
                messages.error(request, "Created {0}".format(form.name), extra_tags="alert")
                return redirect("party_home")    
    else:
        ava_form = AvatarForm()
    return render(request, "create_avatar.html", {"ava_form": ava_form})


@login_required
def avatar_screen(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
    print(ava.cav)
    return render(request, "avatar_screen.html", {"ava": ava})


@login_required
def delete_avatar(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
    if ava.created_by == request.user.profile:
        ava.delete()
        messages.error(
            request, f"Deleted {ava}", extra_tags="alert"
        )
        return redirect(reverse("party_home"))
    else:
        messages.error(request, f"Avatar Not Yours To Delete", extra_tags="alert")
        return redirect("party_home")


@login_required
def rename_avatar(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
    if request.method == "POST":
        ava_form = RenameAvatar(request.POST, instance=ava)
        if ava_form.is_valid():
            form = ava_form.save(commit=False)
            form.save()
            messages.error(request, "Renamed {0}".format(form.name), extra_tags="alert")
            return redirect("avatar_screen", ava.pk)    
    else:
        ava_form = RenameAvatar()
    return render(request, "rename_avatar.html", {"ava_form": ava_form, "ava": ava})


# Caravan 

@login_required
def start_caravan(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
    cav_form = CaravanForm()
    form = cav_form.save(commit=False)
    form.owner = ava
    form.save()
    messages.error(request, "Created {0}'s Caravan".format(ava.name), extra_tags="alert")
    return redirect("avatar_screen", ava.pk)  

