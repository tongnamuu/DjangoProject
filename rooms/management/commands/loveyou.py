from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "This is my Command"

    # print("hello")

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        parser.add_argument(
            "--times", help="How many times do you want me to execute the commands?"
        )

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        times = int(options.get("times"))
        for t in range(0, times):
            # print("I Love YOU")
            self.stdout.write(self.style.WARNING("I Love YOU"))
            # self.stdout.write(self.style.SUCCESS("I Love YOU"))
        # print(args, options)

