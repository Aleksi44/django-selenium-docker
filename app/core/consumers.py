import logging
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

logger = logging.getLogger('app')


class TaskConsumer(WebsocketConsumer):
    task_key_composer = None

    def connect(self):
        self.task_key_composer = self.scope['url_route']['kwargs']['key_composer']
        async_to_sync(self.channel_layer.group_add)(
            self.task_key_composer,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.task_key_composer,
            self.channel_name
        )

    def sync_function(self, event):
        self.send(text_data=json.dumps({
            'screenshot_b64': event['screenshot_b64']
        }))
