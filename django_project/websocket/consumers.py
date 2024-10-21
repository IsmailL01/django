import json
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'message': "GeeksforGeeks"}))
    def disconnect(self, code):
        pass
    
    def receive(self, text_data=None, bytes_data=None):
        pass