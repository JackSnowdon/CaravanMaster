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


@login_required
def avatar_screen(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
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
