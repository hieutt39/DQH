from __future__ import with_statement
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class StreamApi(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["task_name"]
        self.room_group_name = 'group_send'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('text_data_json', text_data_json)
        message = text_data_json["message"]

        print('self.room_group_name', self.room_group_name)
        print('self.channel_layer.group_send', self.channel_layer.group_send)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "send_message", "message": message}
        )

    # Receive message from room group
    def send_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

class StatisticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Tạo kết nối WebSocket
        self.room_group_name = 'statistics'

        # Tham gia group WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Cho phép kết nối
        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi group khi ngắt kết nối
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Nhận message từ group
    async def receive(self, text_data):
        # Lấy thống kê (ví dụ số người online và tổng truy cập)
        online_users = 10  # Thay bằng logic thực tế của bạn
        total_visits = 1000  # Thay bằng logic thực tế của bạn

        # Gửi dữ liệu thống kê cho tất cả client trong group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_statistics',
                'online_users': online_users,
                'total_visits': total_visits,
            }
        )

    # Gửi dữ liệu thống kê cho các WebSocket client
    async def send_statistics(self, event):
        online_users = event['online_users']
        total_visits = event['total_visits']

        # Gửi dữ liệu đến WebSocket client
        await self.send(text_data=json.dumps({
            'online_users': online_users,
            'total_visits': total_visits,
        }))
