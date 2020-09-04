from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def world_index(request):
    locs = Location.objects.order_by('name')
    return render(request, "world_index.html", {"locs": locs})


@login_required
def create_location(request):
    if request.method == "POST":
        loc_form = LocationForm(request.POST)
        if loc_form.is_valid():
            form = loc_form.save(commit=False)
            form.created_by = request.user.profile
            form.save()
            messages.error(request, "Created {0}".format(form.name), extra_tags="alert")
            return redirect("world_index")    
    else:
        loc_form = LocationForm()
    return render(request, "create_location.html", {"loc_form": loc_form})


@login_required
def edit_location(request, pk):
    this_location = get_object_or_404(Location, pk=pk)
    if request.user.profile.staff_access:
        if request.method == "POST":
            loc_form = LocationForm(request.POST, instance=this_location)
            if loc_form.is_valid():
                form = loc_form.save(commit=False)
                form.save()
                messages.error(
                    request, "Edited {0}".format(form.name), extra_tags="alert"
                )
                return redirect("world_index")
        else:
            loc_form = LocationForm(instance=this_location)
        return render(
            request,
            "edit_location.html",
            {"loc_form": loc_form, "this_sheet": this_location},
        )
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")

