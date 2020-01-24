from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Space", {"fields": ("guests", "beds", "bedrooms", "baths",)}),
        (
            "More About the Spaces",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )
    list_display = (
        "name",
        "count_amenities",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    search_fields = (
        "^city",
        "host__username",
    )
    ordering = ("name", "city", "price", "bedrooms")
    # horizontal : manytomany fields에서 사용
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        # self : admin class (RoomAdmin)
        # object : current row
        return obj.amenities.count()

    count_amenities.short_description = "hi tongnamuu!!"
    # count_amenities 가 hi tongnamuu!!로 나타남


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
