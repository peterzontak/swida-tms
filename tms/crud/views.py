from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from app.models import TransportOrder, Waypoint, TransportOrderWaypoint
from app.serializers import WaypointSerializer, TransportOrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status


class TransportOrderDetailView(APIView):
    def get(self, request, id):
        try:
            item = TransportOrder.objects.get(pk=id)
            serializer = TransportOrderSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TransportOrder.DoesNotExist:
            return Response({'error': 'Transport order with id "{id}" not found'}, status=status.HTTP_404_NOT_FOUND)


class WaypointDetailView(APIView):
    def get(self, request, id):
        try:
            item = TransportOrder.objects.get(pk=id)
            serializer = TransportOrderSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TransportOrder.DoesNotExist:
            return Response({'error': 'Transport order with id "{id}" not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def transport_orders_index(request):
    objects = TransportOrder.objects.all()
    serializer = TransportOrderSerializer(objects, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def transport_orders_add(request):
    # TODO: for key, value in request.data.items():
    values = list(request.data.values())
    order_number = values[0] if len(values) > 0 else ''
    customer_name = values[1] if len(values) > 1 else ''
    order_date = values[2] if len(values) > 2 else ''
    waypoints = values[3] if len(values) > 3 else []

    # TODO validation
    transportOrder = TransportOrder.objects.create(order_number=order_number, customer_name=customer_name, order_date=order_date)
    if transportOrder:
        for index, waypoint_id in enumerate(waypoints):
            waypoint = Waypoint.objects.get(id=waypoint_id)
            if waypoint:
                TransportOrderWaypoint.objects.create(
                    transport_order=transportOrder,
                    waypoint=waypoint,
                    order_index=index + 1  # Order index starts from 1
                )
        
        if transportOrder:
            return Response(TransportOrderSerializer(transportOrder).data)
    
    return Response({'success': False})


@api_view(['DELETE'])
def transport_orders_delete(request, id: int):
    try:
        TransportOrder.objects.get(id=id).delete()
        return Response({'success': True, 'id': id}, status=status.HTTP_200_OK)
    except TransportOrder.DoesNotExist:
        return Response({'success': False, 'id': id, 'error': 'Transport order with id "{id}" not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def waypoints_index(request):
    objects = Waypoint.objects.all()
    serializer = WaypointSerializer(objects, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
def waypoints_add(request):
    #TODO: for key, value in request.data.items():
    values = list(request.data.values())
    address = values[0] if len(values) > 0 else ''
    location_name = values[1] if len(values) > 1 else ''
    waypoint_type = values[2] if len(values) > 2 else ''

    # TODO validation
    waypoint = Waypoint.objects.create(address=address, location_name=location_name, type=waypoint_type)
    
    if waypoint:
        return Response(WaypointSerializer(waypoint).data)
    
    return Response({'success': False})


@api_view(['DELETE'])
def waypoint_delete(request, id: int):
    try:
        Waypoint.objects.get(id=id).delete()
        return Response({'success': True, 'id': id}, status=status.HTTP_200_OK)
    except Waypoint.DoesNotExist:
        return Response({'success': False, 'id': id, 'error': 'Transport order with id "{id}" not found'}, status=status.HTTP_404_NOT_FOUND)



# TODO: endpoint for reordering waypoints
# from django.db import transaction
# def reorder_waypoints(order_id, new_order):
#     with transaction.atomic():
#         for index, waypoint_id in enumerate(new_order):
#             Waypoint.objects.filter(id=waypoint_id).update(order_index=index)



@api_view(['get'])
def customers_index(request):
    objects = TransportOrder.objects.all()
    serializer = TransportOrderSerializer(objects, many=True)
    customer_names = [o['customer_name'] for o in serializer.data]
    # customers = [{'customer_name': o['customer_name']} for o in serializer.data]
    unique_customer_names = list(set(customer_names))
    customers = [{'customer_name': name} for name in unique_customer_names]
    
    return Response(customers)

@api_view(['get'])
def filter_by_customer_name(request, customer_name: str):
    # objects = TransportOrder.objects.all()
    objects = TransportOrder.objects.filter(customer_name=customer_name)
    serializer = TransportOrderSerializer(objects, many=True)
    
    return Response(serializer.data)



def filter_by_transport_order_date(from_str: str|None = None, to_str: str|None = None):
    objects = []
    
    try:
        from_date = timezone.datetime.strptime(from_str, '%Y-%m-%d').date() if from_str else None
        to_date = timezone.datetime.strptime(to_str, '%Y-%m-%d').date() if to_str else None
            
        if from_date is not None and to_date is not None:
            objects = TransportOrder.objects.filter(order_date__range=(from_date, to_date))
        elif from_date is not None:
            objects = TransportOrder.objects.filter(order_date__gte=from_date)
        elif to_date is not None:
            objects = TransportOrder.objects.filter(order_date__lte=to_date)
        else:
            objects = TransportOrder.objects.all()
            
    except ValueError:
        return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=400)
    
    serializer = TransportOrderSerializer(objects, many=True)
    
    return Response(serializer.data)

@api_view(['get'])
def filter_by_transport_order_date_from_to(request, from_str: str|None = None, to_str: str|None = None):
    return filter_by_transport_order_date(from_str, to_str)

@api_view(['get'])
def filter_by_transport_order_date_to(request, to_str: str|None = None):
    return filter_by_transport_order_date(None, to_str)
    

