import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test_room'
        
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("--- WebSocket Connected and Group Joined ---")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("--- WebSocket Disconnected ---")

    async def receive(self, text_data):
        print(f"--- Raw Data Received: {text_data} ---")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(f"--- Message sent to Group: {message} ---")

    async def chat_message(self, event):
        message = event['message']
        print(f"--- Broadcasting to Browser: {message} ---")
        
        await self.send(text_data=json.dumps({
            'message': message
        }))







    # async def receive(self, text_data):
        
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

        
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))

       


