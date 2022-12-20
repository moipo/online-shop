import json
from channels.consumer import AsyncConsumer
import asyncio
from time import sleep
from random import randint
import requests
import json

class ExchangeRateConsumer(AsyncConsumer):
    async def websocket_connect(self,event):


        #This free API gives only 1000 requests/month
        #This is why the imitation of frequent API calls is used here.




        try:
            with open("last_websocket_call_time.pickle", "rb") as f:
                last_api_call = pickle.load(f)
            time_diff = int((datetime.now()-last_api_call).total_seconds())
            print(time_diff)
            if time_diff > 10*60:
                with open("last_websocket_call_time.pickle", "wb") as f:
                    pickle.dump(datetime.now(), f)
                    # api call
            else:
                #no api call


        except:
            with open("last_websocket_call_time.pickle", "wb") as f:
                pickle.dump(datetime.now(), f)












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
            await asyncio.sleep(2.2)
            data = str(float('%.2f' % float(a+randint(-15, 15)/100)))
            if data[-2] == ".": data += "0"

            await self.send({
            'type':'websocket.send',
            "text" : data,
            })
