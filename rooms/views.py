from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from . import models
from math import ceil

from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.urls import reverse
from django.http import Http404

from django_countries import countries

from . import forms

# Create your views here.


class HomeView(ListView):
    # https://ccbv.co.uk/projects/Django/2.2/ 참고
    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 3
    ordering = "created"
    context_object_name = "rooms"
    # page_kwarg = "potato"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "apple" url의 pk대신 apple 사용가능


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                # print(form.cleaned_data)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}
                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                filter_args["country"] = country
                if room_type != None:
                    filter_args["room_type"] = room_type
                if price != None:
                    filter_args["price__lte"] = price
                if guests != None:
                    filter_args["guests__gte"] = guests
                if bedrooms != None:
                    filter_args["bedrooms__gte"] = bedrooms
                if baths != None:
                    filter_args["baths__gte"] = baths
                if bool(instant_book) is True:
                    filter_args["instant_book"] = True
                if bool(superhost) is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms,}
                )
        else:
            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form,})


# def search(request):  # below there is manual search function
#     country = request.GET.get("country")
#     if country:
#         form = forms.SearchForm(request.GET)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilities")

#             filter_args = {}
#             if city != "Anywhere":
#                 filter_args["city__startswith"] = city
#             filter_args["country"] = country
#             if room_type != None:
#                 filter_args["room_type"] = room_type
#             if price != None:
#                 filter_args["price__lte"] = price
#             if guests != None:
#                 filter_args["guests__gte"] = guests
#             if bedrooms != None:
#                 filter_args["bedrooms__gte"] = bedrooms
#             if baths != None:
#                 filter_args["baths__gte"] = baths
#             if bool(instant_book) is True:
#                 filter_args["instant_book"] = True
#             if bool(superhost) is True:
#                 filter_args["host__superhost"] = True

#             for amenity in amenities:
#                 filter_args["amenities"] = amenity

#             for facility in facilities:
#                 filter_args["facilities"] = facility

#             rooms = models.Room.objects.filter(**filter_args)

#     else:
#         form = forms.SearchForm()
#     return render(request, "rooms/search.html", {"form": form})


# def room_detail(request, pk):
#     # print(pk)
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()
#         # return redirect("/")
#         # return redirect(reverse("core:home"))


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
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(
#         room_list, 10, orphans=4
#     )  # orphans 이하의 목록은 last page에 합쳐진다, 더 크면 새로운 페이지생성
#     # print(vars(rooms.paginator))
#     # page = paginator.get_page(page)
#     try:
#         # page = paginator.page(page or 1)
#         context_page = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": context_page})
#     except Exception:
#         return redirect("/")

# def search(request):
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")
#     instant = request.GET.get("instant", False)
#     superhost = request.GET.get("superhost", False)
#     form = {
#         "city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "price": price,
#         "guests": guests,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,
#     }
#     # print(s_amenities)
#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     filter_args = {}
#     if city != "Anywhere":
#         filter_args["city__startswith"] = city
#     filter_args["country"] = country
#     if room_type != 0:
#         filter_args["room_type__pk__exact"] = room_type
#     if price != 0:
#         filter_args["price__lte"] = price
#     if guests != 0:
#         filter_args["guests__gte"] = guests
#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms
#     if baths != 0:
#         filter_args["baths__gte"] = baths
#     if bool(instant) is True:
#         filter_args["instant_book"] = True
#     if bool(superhost) is True:
#         filter_args["host__superhost"] = True

#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)

#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facillities__pk"] = int(s_facility)

#     rooms = models.Room.objects.filter(**filter_args)
#     print(filter_args)
#     print(rooms)
#     return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms},)
