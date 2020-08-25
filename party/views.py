from django.shortcuts import render

# Create your views here.

def party_home(request):
    return render(request, "party_home.html")