from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Truncate the TransportOrder table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM app_transportorderwaypoint;")
            cursor.execute("DELETE FROM app_waypoint;")
            cursor.execute("DELETE FROM app_transportorder;")
        self.stdout.write(self.style.SUCCESS('Successfully truncated'))
