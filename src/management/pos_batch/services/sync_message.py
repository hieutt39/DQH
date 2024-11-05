import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

# Define a channel for show realtime
channel_layer = get_channel_layer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SyncMessage:
    def __init__(self):
        self.assets = f'{settings.BASE_DIR}/assets'

    @staticmethod
    def send_message(message):
        async_to_sync(channel_layer.group_send)("group_send",
                                                {
                                                    "type": "send_message",
                                                    "message": message
                                                })
