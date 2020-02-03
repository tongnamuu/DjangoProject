from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from . import models
from math import ceil

from django.core.paginator import Paginator, EmptyPage

# Create your views here.

# def all_rooms(request):
#     now = datetime.now()
#     return HttpResponse(content=f"hello {now}")
# def all_rooms(request):
#     now = datetime.now()
#     hungry = False
#     return render(request, "all_rooms.html", context={"now": now, "hungry": hungry,})

# manual paginator
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     page = int(page or 1)
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count + 1),
#         },
#     )
# using django paginator
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(
        room_list, 10, orphans=4
    )  # orphans 이하의 목록은 last page에 합쳐진다, 더 크면 새로운 페이지생성
    # print(vars(rooms.paginator))
    # page = paginator.get_page(page)
    try:
        # page = paginator.page(page or 1)
        context_page = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": context_page})
    except Exception:
        return redirect("/")
