from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from . import models

# Create your views here.

# def all_rooms(request):
#     now = datetime.now()
#     return HttpResponse(content=f"hello {now}")
# def all_rooms(request):
#     now = datetime.now()
#     hungry = False
#     return render(request, "all_rooms.html", context={"now": now, "hungry": hungry,})


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
