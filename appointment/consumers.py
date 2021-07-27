
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class  TestConsumer(AsyncJsonWebsocketConsumer):
   async def connect(self):
      await self.accept()
   
   async def receive_json(self, content, **kwargs):
      data = content
      if data['command']=='join':
         await self.channel_layer.group_add(
            data['groupname'],
            self.channel_name
         )
         print("useradded")
   async def disconnect(self, msg):
      pass
      
