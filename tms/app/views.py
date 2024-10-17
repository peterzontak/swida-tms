from django.shortcuts import render, HttpResponse
from . models import TransportOrder, Waypoint
from . serializers import WaypointSerializer, TransportOrderSerializer

def home(request):
    return render(request, 'home.html')


def transport_orders(request):
    objects = TransportOrder.objects.all()
    serializer = TransportOrderSerializer(objects, many=True)
    return render(request, 'transport_orders.html', {'transport_orders': serializer.data})

def waypoints(request):
    objects = Waypoint.objects.all()
    serializer = WaypointSerializer(objects, many=True)
    return render(request, 'waypoints.html', {'waypoints': serializer.data})




