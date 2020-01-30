import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from rooms.models import Room
from users import models as user_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many fake rooms are you going to create?",
        )

    def handle(self, *args, **options):
        all_user = user_models.User.objects.all()  # not good way if user is big
        room_types = room_models.RoomType.objects.all()
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "guests": lambda x: random.randint(0, 20),
                "beds": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))

