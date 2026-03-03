import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
now = datetime.datetime.now()

def receive_weather():
    yahoo_url = "https://map.yahooapis.jp/weather/V1/place?appid={appid}&coordinates={lat_lon}&output={output}&date={date}"
    yahoo_url = yahoo_url.format(appid=os.environ['YAHOO_APPID'], lat_lon=os.environ['YAHOO_COORDINATES'], output="json",
                             date=now.strftime("%Y%m%d%H%M"))
    yahoo_json = requests.get(yahoo_url).json()
    yahoo_rainfall = yahoo_json["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Rainfall"]
    return yahoo_rainfall

rain = receive_weather()
print(rain)