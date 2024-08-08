import json
from channels.generic.websocket import WebsocketConsumer # type: ignore
from asgiref.sync import async_to_sync

class ECGConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'ecg_data'
        self.room_group_name = 'ecg_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bpm = text_data_json['bpm']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'ecg_data',
                'bpm': bpm
            }
        )

    def ecg_data(self, event):
        bpm = event['bpm']

        self.send(text_data=json.dumps({
            'bpm': bpm
        }))
