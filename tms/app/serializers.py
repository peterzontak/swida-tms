from rest_framework import serializers
from .models import TransportOrder, Waypoint, TransportOrderWaypoint

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = ['id', 'location_name', 'address', 'type']

class TransportOrderWaypointSerializer(serializers.ModelSerializer):
    waypoint = WaypointSerializer()  # Serialize the Waypoint details

    class Meta:
        model = TransportOrderWaypoint
        fields = ['waypoint', 'order_index']  # Include waypoint and order_index

class TransportOrderSerializer(serializers.ModelSerializer):
    waypoints = TransportOrderWaypointSerializer(many=True)  # Use the new serializer

    class Meta:
        model = TransportOrder
        fields = ['id', 'order_number', 'customer_name', 'order_date', 'waypoints']

    def create(self, validated_data):
        waypoints_data = validated_data.pop('waypoints')
        transport_order = TransportOrder.objects.create(**validated_data)
        
        for waypoint_data in waypoints_data:
            waypoint_instance = waypoint_data.pop('waypoint')
            waypoint_obj = Waypoint.objects.get(id=waypoint_instance['id'])  # Assuming you're passing existing waypoints
            TransportOrderWaypoint.objects.create(transport_order=transport_order, waypoint=waypoint_obj, **waypoint_data)
        
        return transport_order

    def update(self, instance, validated_data):
        waypoints_data = validated_data.pop('waypoints')
        instance.order_number = validated_data.get('order_number', instance.order_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.save()

        # Update waypoints
        for waypoint_data in waypoints_data:
            waypoint_instance = waypoint_data.pop('waypoint')
            waypoint_obj = Waypoint.objects.get(id=waypoint_instance['id'])
            order_waypoint, created = TransportOrderWaypoint.objects.update_or_create(
                transport_order=instance,
                waypoint=waypoint_obj,
                defaults={'order_index': waypoint_data['order_index']}
            )

        return instance


