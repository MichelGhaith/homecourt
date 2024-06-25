from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ballhandling/", consumers.BallHandlingConsumer.as_asgi()),
    path("reaction/",consumers.ReactionDrillConsumer.as_asgi()),
    path("agility/", consumers.AgilityDrillConsumer.as_asgi()),
]