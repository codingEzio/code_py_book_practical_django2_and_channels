from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import product in BookTime"

    def handle(self, *args, **options):
        """ The logic code will be put in here.
        """

        self.stdout.write("Importing products ..")