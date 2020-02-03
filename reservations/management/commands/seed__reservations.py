from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from reservations import models as reservation_models
from rooms import models as room_models
from users import models as user_models
import random
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):

    help = "This command created reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many fake reservations are you going to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: timezone.now().date(),
                "check_out": lambda x: timezone.now().date()
                + timedelta(days=random.randint(1, 25)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} reservations created!"))

