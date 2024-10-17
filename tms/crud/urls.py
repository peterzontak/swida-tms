from django.urls import path
from config.frontend import load_config
from django.urls import re_path
from . import views

config = load_config()
resources = config['api']['resources']
transport_order_resource = resources['transport_order']
waypoint_resource = resources['waypoint']
customer_resource = resources['customer']




urlpatterns = [
    # Transport Order Resource
    path(transport_order_resource['index'], views.transport_orders_index, name="transport-orders.index"),
    # TODO: path(transport_order_resource['show'] + '/<int:id>/', views.transport_orders_show, name='transport-orders.show'),
    path(transport_order_resource['add'], views.transport_orders_add, name='transport-orders-add'),
    path(transport_order_resource['delete'] + '/<int:id>/', views.transport_orders_delete, name='transport-orders-delete'),
    
    # Waypoint Resource
    path(waypoint_resource['index'], views.waypoints_index, name="waypoints.index"),
    # TODO: path(waypoint_resource['show'] + '/<int:id>/', views.waypoint_show, name='waypoints.show'),
    path(waypoint_resource['add'], views.waypoints_add, name='waypoints-add'),
    path(waypoint_resource['delete'] + '/<int:id>/', views.waypoint_delete, name='waypoint-resource-delete'),

    # Customer Resource
    path(customer_resource['index'], views.customers_index, name="customers.index"),
    
    # filters
    path(transport_order_resource['filters']['customer_name'] + '/<str:customer_name>/', views.filter_by_customer_name, name="filter.customer_name"),
    
    path(f'{transport_order_resource["filters"]["transport_order_date_from_to"]}/', views.filter_by_transport_order_date_from_to),
    path(f'{transport_order_resource["filters"]["transport_order_date_from"]}/<str:from_str>/', views.filter_by_transport_order_date_from_to, name="filter.transport_order_date_no_to"),
    path(f'{transport_order_resource["filters"]["transport_order_date_to"]}/<str:to_str>/', views.filter_by_transport_order_date_to, name="filter.transport_order_date_no_from"),
    path(f'{transport_order_resource["filters"]["transport_order_date_from_to"]}/<str:from_str>/<str:to_str>/', views.filter_by_transport_order_date_from_to, name="filter.transport_order_date_from_to")

]
