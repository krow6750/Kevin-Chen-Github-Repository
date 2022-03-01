from bs4 import BeautifulSoup as Soup
import requests
url = "https://www.7timer.info/bin/astro.php?lon=113.2&lat=23.1&ac=0&unit=metric&output=json&tzshift=0"
response = requests.get(url)
soup = Soup(response.content)  # content is bytes object
for li in soup.find_all('li'):
   print(li)

def getWeather(highTemp, lowTemp, avgTemp):
    earthquakedict ={
    "highTemp" : highTemp,
    "lowTemp" : lowTemp,
    "avgTemp" : avgTemp
    }

def main():
    request.get()
    getWeather()
