from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from party.models import *
from party.forms import HireCrewForm

# Create your views here.

# Location Backend

@login_required
def world_index(request):
    locs = Location.objects.order_by('-population')
    shops = Shop.objects.all()
    loc_shops = shops.exclude(location__name__isnull=True).order_by('location__name')
    nomad_shops = shops.exclude(location__name__isnull=False)
    return render(request, "world_index.html", {"locs": locs, "loc_shops": loc_shops, "nomad_shops": nomad_shops})


@login_required
def create_location(request):
    if request.user.profile.staff_access:
        if request.method == "POST":
            loc_form = LocationForm(request.POST)
            if loc_form.is_valid():
                form = loc_form.save(commit=False)
                form.created_by = request.user.profile
                form.save()
                messages.error(request, f"Created {form.name}", extra_tags="alert")
                return redirect("world_index")    
        else:
            loc_form = LocationForm()
        return render(request, "create_location.html", {"loc_form": loc_form})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")


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
                    request, f"Edited {form.name}", extra_tags="alert"
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


@login_required
def delete_location(request, pk):
    if request.user.profile.staff_access:
        this_location = get_object_or_404(Location, pk=pk)
        this_location.delete()
        messages.error(
            request, f"Deleted {this_location}", extra_tags="alert"
        )
        return redirect("world_index")
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")


# Location 

@login_required
def location(request, pk):
    ava = get_current_save(request.user.profile)
    loc = get_object_or_404(Location, pk=pk)
    return render(request, "location.html", {"loc": loc, "ava": ava})


# Campground

@login_required
def create_camp(request, pk):
    if request.user.profile.staff_access:
        loc = get_object_or_404(Location, pk=pk)
        camp_form = CampgroundForm()
        form = camp_form.save(commit=False)
        form.gold = 1000
        form.location = loc
        form.save()
        messages.error(request, f"Created {loc}'s Campground", extra_tags="alert")
        return redirect("world_index")
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")


@login_required
def campground(request, pk):
    ava = get_current_save(request.user.profile)
    camp = get_object_or_404(Campground, pk=pk)
    return render(request, "campground.html", {"camp": camp, "ava": ava})


@login_required
def edit_campground(request, pk):
    camp = get_object_or_404(Campground, pk=pk)
    return render(request, "edit_campground.html", {"camp": camp})

@login_required
def hire_merc(request, pk, locpk):
    crew = get_object_or_404(MemberBase, pk=pk)
    ava = get_current_save(request.user.profile)
    loc = get_object_or_404(Location, pk=locpk)
    if ava.cav.guard.count() >= ava.cav.size:
        messages.error(request, f"{ava.cav} Is Full ({ava.cav.size})", extra_tags="alert")
        return redirect("campground", loc.pk)
    if ava.gold < crew.cost:
        messages.error(request, f"{ava} Can't Afford {crew} ({crew.cost}) Gold", extra_tags="alert")
        return redirect("campground", loc.pk)
    else:
        ava.gold -= crew.cost
        ava.save()
        camp = loc.camp
        camp.gold += crew.cost
        camp.save()
        crew_form = HireCrewForm()
        form = crew_form.save(commit=False)
        form.base = crew
        form.max_hp = 100 + form.base.level * 10 + form.base.defense * 3
        form.current_hp = form.max_hp
        form.hired_by = ava
        form.assigned_to = ava.cav
        form.save()
        messages.error(request, f"{ava} Hired {crew}, Assigned To {ava.cav}", extra_tags="alert")
        return redirect("campground", loc.pk)


# Shop

@login_required
def create_shop(request):
    if request.user.profile.staff_access:
        if request.method == "POST":
            shop_form = ShopForm(request.POST)
            if shop_form.is_valid():
                form = shop_form.save(commit=False)
                if form.location != None:
                    loc = form.location
                    shops = loc.shops.all()
                    for s in shops:
                        if form.shop_type == s.shop_type:
                            messages.error(request, f"{loc} Already Has A {form}", extra_tags="alert")
                            return redirect("world_index")   
                form.save()
                messages.error(request, f"New Shop Created", extra_tags="alert")
                return redirect("world_index")    
        else:
            shop_form = ShopForm()
        return render(request, "create_shop.html", {"shop_form": shop_form})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")


@login_required
def delete_shop(request, pk):
    if request.user.profile.staff_access:
        this_shop = get_object_or_404(Shop, pk=pk)
        this_shop.delete()
        messages.error(
            request, f"Deleted {this_shop}", extra_tags="alert"
        )
        return redirect("world_index")
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("index")


@login_required
def shop(request, pk):
    ava = get_current_save(request.user.profile)
    shop = get_object_or_404(Shop, pk=pk)
    return render(request, "shop.html", {"shop": shop, "ava": ava})


# Helper Functions

def get_current_save(p):
    """
    Takes request.user.profile and returns Avatar
    """
    save = p.current_save
    ava = get_object_or_404(Avatar, pk=save)
    return ava

    

# Movement 

