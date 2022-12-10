import json
from channels.consumer import AsyncConsumer
import asyncio
from time import sleep
from random import randint
import requests
import json

class ExchangeRateConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
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
