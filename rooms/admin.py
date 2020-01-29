from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    inlines = (PhotoInline,)
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
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
        "count_photos",
        "total_rating",
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

    raw_id_fields = ("host",)

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

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        # print(dir(obj.file))
        return mark_safe(f'<img width="50px" src ="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"
