from django.core.management.base import BaseCommand

from functions import init_db, clear_table


def fill_db():
    clear_table()
    init_db()


class Command(BaseCommand):
    help = "Initialize the app database !"

    def handle(self, **options):
        fill_db()
        # Send a message in de console
        message = "\n\nWARNINGS !!! Database initialized...\n\n"
        self.stdout.write(self.style.SUCCESS(message))
