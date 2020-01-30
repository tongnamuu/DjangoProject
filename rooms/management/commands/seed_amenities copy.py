from django.core.management.base import BaseCommand
from rooms import models as room_models
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This will create Amenities in rooms"

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check_in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
            "Beachfront",
            "Waterfront",
            "Ski_in & ski_out",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities Created"))
