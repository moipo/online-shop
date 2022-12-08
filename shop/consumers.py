import json
from channels.generic.websocket import WebsocketConsumer
from time import sleep
from random import randint

class ExchangeRateConsumer(WebsocketConsumer):
    def connect(self):
        print("it worked")
        self.accept()
        a = 80
        while True:
            sleep(1)
            a+=randint(-1, 1)
            self.send(text_data = json.dumps({
            "data" : str(a),
            }))
