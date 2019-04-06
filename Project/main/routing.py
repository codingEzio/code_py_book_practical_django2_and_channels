from django.urls import path

from . import consumers


# ~= main/urls.py
websocket_urlpatterns = [
    path(
        "ws/customer-service/<int:order_id>/",
        consumers.ChatConsumer
    )
]
