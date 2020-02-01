from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from . import models
from math import ceil

# Create your views here.

# def all_rooms(request):
#     now = datetime.now()
#     return HttpResponse(content=f"hello {now}")
# def all_rooms(request):
#     now = datetime.now()
#     hungry = False
#     return render(request, "all_rooms.html", context={"now": now, "hungry": hungry,})


def all_rooms(request):
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
