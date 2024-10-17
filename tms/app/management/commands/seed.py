import random
from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker
from django.utils import timezone
from app.models import TransportOrder, Waypoint, TransportOrderWaypoint  # Adjust the import based on your app structure

class Command(BaseCommand):
    help = 'Seed dummy transport orders'

    def handle(self, *args, **kwargs):
        call_command('truncate_all')
        fake = Faker()

        # Create dummy TransportOrder instances first
        orders = []
        for _ in range(10):  # Create 10 dummy transport orders
            order = TransportOrder.objects.create(
                order_number=str(_) + timezone.now().strftime("%Y%m%d"),
                customer_name=fake.name(),
                order_date=fake.date_this_year()
            )
            orders.append(order)

        # Now, create some dummy Waypoint instances and associate them with the orders using TransportOrderWaypoint.
        for order in orders:
            num_waypoints = random.randint(1, 5)  # Randomly decide how many waypoints to create for this order
            waypoints = []

            for _ in range(num_waypoints):
                if random.choice([True, False]):
                    location_name = None  # There is a 50% chance that the location name will remain empty.
                else:
                    location_name = fake.company()
                waypoint = Waypoint.objects.create(
                    location_name=location_name,
                    address=fake.address(),
                    type=random.choice(['pickup', 'delivery']),
                )
                waypoints.append(waypoint)  # Store created waypoint

            # Associate waypoints with the current order using TransportOrderWaypoint
            for index, waypoint in enumerate(waypoints):
                TransportOrderWaypoint.objects.create(
                    transport_order=order,
                    waypoint=waypoint,
                    order_index=index + 1  # Order index starts from 1
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded dummy transport orders with waypoints'))
