from django.core.management.base import BaseCommand
from rooms import models as room_models
from rooms.models import Facility


class Command(BaseCommand):

    help = "This will create facilities in rooms"

    def handle(self, *args, **options):
        facilities = [
            "Elevator",
            "Privated entrance",
            "Parking",
            "Free parking on premises",
            "Paid parking on premises",
            "Paid parking off premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("Facilities Created"))
