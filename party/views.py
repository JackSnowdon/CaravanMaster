from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from world.models import Location

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
    loc = get_object_or_404(Location, name="HomeVilled")
    form.currently_at = loc
    form.owner = ava
    form.save()
    messages.error(request, "Created {0}'s Caravan".format(ava.name), extra_tags="alert")
    return redirect("avatar_screen", ava.pk)


@login_required
def caravan(request, pk):
    cav = get_object_or_404(Caravan, pk=pk)
    ava = cav.owner
    crew = ava.crew.all().filter(assigned_to=None).order_by('base__name')
    guard = cav.guard.all().order_by('base__name')
    return render(request, "caravan.html", {"cav": cav, "crew": crew, "guard": guard})


@login_required
def assign_crew_to_caravan(request, crewpk, cavpk):
    crew = get_object_or_404(CrewMember, pk=crewpk)
    cav = get_object_or_404(Caravan, pk=cavpk)
    if crew.assigned_to != None:
        crew.assigned_to = None
        messages.error(request, f"{crew} Removed From {cav}", extra_tags="alert")
    else:
        crew.assigned_to = cav
        messages.error(request, f"{crew} Added To {cav}", extra_tags="alert")
    crew.save()
    return redirect("caravan", cav.pk)


# Members Backend

@login_required
def member_home(request):
    mems = MemberBase.objects.order_by('name')
    return render(request, "member_home.html", {"mems": mems})


@login_required
def create_member_base(request):
    if request.method == "POST":
        mem_form = CreateMemberBase(request.POST)
        if mem_form.is_valid():
            form = mem_form.save(commit=False)
            point_limit = form.level * 10
            point_total = form.attack + form.defense + form.intel
            if point_total > point_limit:
                messages.error(request, f"Point Total ({point_total}) Above Level Limit ({point_limit})", extra_tags="alert")
            else:
                form.save()
                messages.error(request, "Created {0}".format(form.name), extra_tags="alert")
                return redirect("member_home")    
    else:
        mem_form = CreateMemberBase()
    return render(request, "create_member_base.html", {"mem_form": mem_form})


@login_required
def delete_member_base(request, pk):
    this_crew = get_object_or_404(MemberBase, pk=pk)
    this_crew.delete()
    messages.error(
            request, f"Deleted {this_crew}", extra_tags="alert"
        )
    return redirect("member_home")


@login_required
def member_base(request, pk):
    mem = get_object_or_404(MemberBase, pk=pk)
    return render(request, "member_base.html", {"mem": mem})


# Crew

@login_required
def crew(request, pk):
    ava = get_object_or_404(Avatar, pk=pk)
    mems = MemberBase.objects.order_by('name')
    crew = ava.crew.all().order_by('base__name')
   # ncrew = return_grouped_crew(crew)
  #  print(ncrew)
    return render(request, "crew.html", {"mems": mems, "ava": ava, "crew": crew})


def return_grouped_crew(crew):
    returned_dict = {}
    for i, c in enumerate(crew):
        result = crew.filter(base=c.base)
        if c in returned_dict:
            break
        returned_dict[c] = result.count()
    return returned_dict


@login_required
def hire_crew(request, crewpk, avapk):
    crew = get_object_or_404(MemberBase, pk=crewpk)
    ava = get_object_or_404(Avatar, pk=avapk)
    if ava.gold < crew.cost:
        messages.error(request, f"{ava} Can't Afford {crew} ({crew.cost}) Gold", extra_tags="alert")
        return redirect("crew", ava.pk)
    else:
        ava.gold -= crew.cost
        ava.save()
        crew_form = HireCrewForm()
        form = crew_form.save(commit=False)
        form.base = crew
        form.hired_by = ava
        form.save()
        messages.error(request, f"{ava} Hired {crew}", extra_tags="alert")
        return redirect("crew", ava.pk)
    

@login_required
def fire_crew(request, crewpk, avapk):
    ava = get_object_or_404(Avatar, pk=avapk)
    this_crew = get_object_or_404(CrewMember, pk=crewpk)
    ava.gold += this_crew.base.cost / 2
    ava.save()
    this_crew.delete()
    messages.error(
            request, f"Fired {this_crew}", extra_tags="alert"
        )
    return redirect("crew", ava.pk)


@login_required
def crew_member(request, pk):
    mem = get_object_or_404(CrewMember, pk=pk)
    ava = mem.hired_by
    return render(request, "crew_member.html", {"mem": mem, "ava": ava})

