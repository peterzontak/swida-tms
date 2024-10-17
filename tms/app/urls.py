from django.urls import path
from config.frontend import load_config
from . import views

config = load_config()

urlpatterns = [
    path('', views.home, name="home"),
    path(config['routes']['transport_orders'], views.transport_orders, name="transport_orders"),
    path(config['routes']['waypoints'], views.waypoints, name="waypoints"),
]
