# tools/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/tools/(?P<task_name>\w+)/$", consumers.StreamApi.as_asgi()),
    re_path(r"ws/statistics/$", consumers.StatisticsConsumer.as_asgi()),
]

