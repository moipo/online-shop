import json
from channels.consumer import AsyncConsumer
import asyncio
from time import sleep
from random import randint
import requests
import json

class ExchangeRateConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("it worked")
        # await self.accept()
        a = 63.15

        try:
            latest_link = "https://openexchangerates.org/api/latest.json"
            app_id = "?app_id=230c6dfde9e04b19a187f83b726fdbc9"
            response = requests.get(latest_link + app_id)
            data = json.loads(response.text)
            a = round(float(data["rates"]["RUB"]),2)
        except:
            a = 63.15

        await self.send({
        'type':'websocket.accept'})

        while True:
            await asyncio.sleep(1.8)
            data = str(float('%.2f' % float(a+randint(-15, 15)/100)))
            if data[-2] == ".": data += "0"

            await self.send({
            'type':'websocket.send',
            "text" : data,
            })




























# import json
# from channels.generic.websocket import WebsocketConsumer
# from time import sleep
# from random import randint
# import requests
# import json
#
# class ExchangeRateConsumer(WebsocketConsumer):
#     def connect(self):
#         print("it worked")
#         self.accept()
#         a = 63.15
#
#         try:
#             latest_link = "https://openexchangerates.org/api/latest.json"
#             app_id = "?app_id=230c6dfde9e04b19a187f83b726fdbc9"
#             response = requests.get(latest_link + app_id)
#             data = json.loads(response.text)
#             a = round(float(data["rates"]["RUB"]),2)
#         except:
#             a = 63.15
#
#
#         while True:
#             sleep(1.8)
#             data = str(float('%.2f' % float(a+randint(-15, 15)/100)))
#             if data[-2] == ".": data += "0"
#
#             self.send(text_data = json.dumps({
#             "data" : data,
#             }))















    # def receive(self, text_data):
    #     print(text_data)
    #     a = 63.15
    #
    #     try:
    #         latest_link = "https://openexchangerates.org/api/latest.json"
    #         app_id = "?app_id=230c6dfde9e04b19a187f83b726fdbc9"
    #         response = requests.get(latest_link + app_id)
    #         data = json.loads(response.text)
    #         a = round(float(data["rates"]["RUB"]),2)
    #     except:
    #         a = 63.15
    #
    #
    #     while True:
    #         sleep(1.8)
    #         data = str(float('%.2f' % float(a+randint(-15, 15)/100)))
    #         if data[-2] == ".": data += "0"
    #
    #         self.send(text_data = json.dumps({
    #         "data" : data,
    #         }))
