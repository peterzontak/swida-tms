from django.db import models

class TransportOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=255)
    order_date = models.DateField()

    def __str__(self):
        return f"Order {self.order_number} for {self.customer_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'order_date': self.order_date,
            'waypoints': [waypoint.to_dict() for waypoint in self.waypoints.all()],
        }

class Waypoint(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]

    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, unique=True)
    location_name = models.CharField(max_length=100, null=True, unique=True)
    type = models.CharField(max_length=10, choices=LOCATION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.location_name if self.location_name else self.address}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'address': self.address,
            'type': self.type,
        }

class TransportOrderWaypoint(models.Model):
    transport_order = models.ForeignKey(TransportOrder, on_delete=models.CASCADE, related_name='waypoints')
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE)
    order_index = models.PositiveIntegerField()

    class Meta:
        unique_together = ('transport_order', 'waypoint')
        ordering = ['order_index']

    def __str__(self):
        return f"{self.transport_order} - {self.waypoint} (Index: {self.order_index})"
