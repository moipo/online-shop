import json
from channels.consumer import AsyncConsumer
import asyncio
from time import sleep
from random import randint
import requests
import json
from .models import WebsocketInfo
from asgiref.sync import sync_to_async
from datetime import datetime, timezone

class ExchangeRateConsumer(AsyncConsumer):
    async def websocket_connect(self,event):

        #This free API gives only 1000 requests/month
        #This is why the imitation of frequent API calls is used here.
        info = await sync_to_async(WebsocketInfo.objects.get)(id=1)

        diff = (datetime.now(timezone.utc) - info.last_usd_datetime).total_seconds()

        # api call every 20 minutes
        if diff >= 10*20:
            exchange_rate = await sync_to_async(get_api_data)()
            info.last_usd_exchange_rate = exchange_rate
            info.last_usd_datetime = await sync_to_async(datetime.now)(timezone.utc)
            await sync_to_async(info.save)()
        else:
            exchange_rate = info.last_usd_exchange_rate

        await self.send({
        'type':'websocket.accept'
        })

        while True:
            await asyncio.sleep(0.7)
            data = str(float('%.2f' % float(exchange_rate+randint(-9, 9)/100)))
            if data[-2] == ".": data += "0"

            await self.send({
            'type':'websocket.send',
            "text" : data,
            })
            await asyncio.sleep(2.2)


def get_api_data():
    try:
        print("[INFO] api was called")
        latest_link = "https://openexchangerates.org/api/latest.json"
        app_id = "?app_id=230c6dfde9e04b19a187f83b726fdbc9"
        response = requests.get(latest_link + app_id)
        data = json.loads(response.text)
        a = round(float(data["rates"]["RUB"]),2)
        return a
    except:
        return 70
