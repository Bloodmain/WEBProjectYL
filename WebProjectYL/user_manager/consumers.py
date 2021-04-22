import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_authenticated:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.chat = Chat.objects.get(pk=self.room_id)
            self.room_group_id = f'chat_{self.room_id}'
            self.user = self.scope['user']
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_id,
                self.channel_name
            )

            self.accept()

            messages = [[msg.text, msg.author.pk, msg.author.profile.get_full_name(), str(msg.create_date)]
                        for msg in Message.objects.filter(chat=self.room_id).order_by('-create_date')]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_id,
                {
                    'type': 'chat_message',
                    'messages': messages,
                    'username': self.user.profile.get_full_name()
                }
            )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )

    def receive(self, text_data):
        "Отсюда он идет в chat_message"
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        Message.objects.create(text=message, author=self.user, chat=self.chat)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.profile.get_full_name()
            }
        )

    def chat_message(self, event):
        "А от сюда уже шлет сообщение"
        if 'messages' in event:
            self.send(text_data=json.dumps({
                'messages': event['messages'],
                'username': event['username']
            }))
        else:
            message = event['message']
            self.send(text_data=json.dumps({
                'message': message,
                'username': event['username']
            }))