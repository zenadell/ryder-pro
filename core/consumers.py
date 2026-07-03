import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.convo_id = self.scope['url_route']['kwargs']['convo_id']
        self.room_group_name = f'chat_{self.convo_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (from client)
    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type')
        
        if msg_type == 'typing':
            # Send typing event to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'role': data.get('role', 'user'),
                    'is_typing': data.get('is_typing', True)
                }
            )

    # Receive typing event from room group
    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'role': event['role'],
            'is_typing': event['is_typing']
        }))
        
    # Receive message from room group (triggered by views)
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'role': event['role'],
            'created_at': event['created_at']
        }))
