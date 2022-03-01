"""
Course:        DCS 211
Assignment:    Project 2a
Purpose:       Use the USGS API to determine info about recorded earthquakes over a specified start date, end date, longitude, latitude, and radius

Student Name: Kevin Chen
Partner Name: Ethan Wu

Other students outside my pair that I received help from ('N/A' if none):
    N/A

Other students outside my pair that I gave help to ('N/A' if none):
    N/A

Citations/links of external references used ('N/A' if none):
    w3schools.com
    stackoverflow.com
"""
# ! pip install geopy requests bs4 progress tqdm
import json
import requests
import time
import datetime
import geopy.geocoders
from tqdm import *
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

geopy.geocoders.options.default_user_agent = "dcs211_kchen@bates.edu/1"
geopy.geocoders.options.default_timeout = 10
nl = '\n'


def makeRequest(url, payload):
    try:
        response = requests.get(url, params=payload)

        if response.status_code in [404, 500, 503, 400]:
            raise SystemExit("Website is down :" + str(response.status_code))
        elif response.status_code == 429:
            raise SystemExit("Too many requests, please try again later")

    except (requests.exceptions.Timeout):
        raise SystemExit("Website is down")

    else:
        return response.json()


def printQuakes(startDate: str, endDate: str, minMagnitude: float) -> str:
    if (not isValidDate(startDate)) or (not isValidDate(endDate)) or (startDate > endDate):
        print(
            f"start date {startDate} and end date {endDate} must be:{nl}valid dates in YYYY-MM-DD format{nl}with start date <= end date{nl}start date <= today's date")
        return
    if (not isValidQuantity(minMagnitude)):
        print(f"minimum magnitude {minMagnitude} must be:{nl}valid minimum magnitude")
        return
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    payload = {
        "format": "geojson",
        "starttime": startDate,
        "endtime": endDate,
        "minmagnitude": minMagnitude,
    }
    status = makeRequest(url, payload)
    if (status[0]):
        return status[1]
    response = requests.get(url, params=payload)
    result = response.json()
    print(f"All earthquakes of magnitude {minMagnitude} or greater between {startDate} and {endDate}:")
    printQuakeInfo(result)


def isValidDate(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        if date > str(datetime.datetime.now().date()):
            return False
        return True
    except ValueError:
        return False


def isValidQuantity(arg) -> bool:
    try:
        float(arg)
        return arg > 0
    except ValueError:
        return False


def isValidLatLong(lat, long):
    try:
        float(lat)
        float(long)
        return (lat >= -90 and lat <= 90) and (long >= -180 and long <= 180)
    except ValueError:
        return False


def printQuakesByLatLong(startDate: str, endDate: str, latitude: float, longitude: float, radius: float):
    if (not isValidLatLong(latitude, longitude)):
        print(f"Latitude {latitude} must be in (-90,90) and longitude {longitude} in (-180,180).")
        return
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    payload = {
        "format": "geojson",
        "starttime": startDate,
        "endtime": endDate,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": radius
    }
    print(payload)
    status = makeRequest(url, payload)
    print(f"All earthquakes within {radius} kilometers of ({longitude},{latitude}) between {startDate} and {endDate}:")
    printQuakeInfo(status)


def printQuakeInfo(result):
    for i in result['features']:
        mag = i['properties']['mag']
        t = datetime.datetime.utcfromtimestamp(i['properties']['time'] / 1e3).replace(tzinfo=datetime.timezone.utc)
        loc = i['properties']['place']
        print(f"magnitude {mag:1.1f} earthquake on {t.strftime('%Y-%m-%d')} @ {t.strftime('%H:%M')} UTC @ {loc}")


def printQuakesByAddress(startDate: str, endDate: str, address: str, radius: float) -> str:
    location = Nominatim().geocode(address)
    printQuakesByLatLong(startDate, endDate, location.latitude, location.longitude, radius)


def getStateCapitals(html_fname: str):
    url = html_fname
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    capitals = []
    tables = soup.find_all('table', {'class': 'wikitable plainrowheaders sortable'})
    for rows in tables:
        row = rows.find_all('th', {'scope': 'row'})
        for capital in row:
            capitals.append(capital.find('a')['title'])
    return (capitals)


def getLatLong(address: str) -> tuple:
    location = Nominatim().geocode(address)
    return (location.latitude, location.longitude)


def getLatLongDict(dict_fname: str, capitals, ) -> dict:
    coords = []
    match = {}
    i = 0
    for capital in tqdm(capitals, desc='Processing capitals'):
        match[capitals[i]] = getLatLong(capital)
        i += 1
    return match


def getQuakes(start_date: str, end_date: str, latitude, longitude, radiuskm):
    if (not isValidLatLong(latitude, longitude)):
        print(f"Latitude {latitude} must be in (-90,90) and longitude {longitude} in (-180,180).")
        return
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    payload = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": radiuskm
    }
    status = makeRequest(url, payload)
    return status


def minMaxNPrint(earfquakes, radiuskm):
    magMin = 99.0
    magMax = -99.0
    tMax = locMax = capMax = magMin = tMin = locMin = capMin = 0
    largestQuake = {}
    smallestQuake = {}
    for capital, data in tqdm(earfquakes.items(), desc="finding extreme quakes"):
        for i in data:
            if i['properties']['mag'] > magMax:
                largestQuake = i
                magMax = i['properties']['mag']
                tMax = datetime.datetime.utcfromtimestamp(i['properties']['time'] / 1e3).replace(
                    tzinfo=datetime.timezone.utc)
                locMax = largestQuake['properties']['place']
                capMax = capital
            if i['properties']['mag'] < magMin:
                smallestQuake = i
                magMin = i['properties']['mag']
                tMin = datetime.datetime.utcfromtimestamp(i['properties']['time'] / 1e3).replace(
                    tzinfo=datetime.timezone.utc)
                locMin = smallestQuake['properties']['place']
                capMin = capital
    print(
        f"minimum magnitude earthquake occurred within {radiuskm} of {capMin}:{nl}magnitude {magMin:1.1f} on {tMin.strftime('%Y-%m-%d')} @ {tMin.strftime('%H:%M')} @ {locMin}")
    print(
        f"maximum magnitude earthquake occurred within {radiuskm} of {capMax}:{nl}magnitude {magMax:1.1f} on {tMax.strftime('%Y-%m-%d')} @ {tMax.strftime('%H:%M')} @ {locMax}")


def printUSQuakeExtremes(lat_long_dict: dict, start_date: str, end_date: str, radiuskm: float) -> None:
    if (not isValidDate(start_date)) or (not isValidDate(end_date)) or (start_date > end_date):
        print(
            f"start date {start_date} and end date {end_date} must be:{nl}valid dates in YYYY-MM-DD format{nl}with start date <= end date{nl}start date <= today's date")
        return
    allQuakes = {}
    for loc, coord in tqdm(lat_long_dict.items(), desc="processing capitals"):
        result = getQuakes(start_date, end_date, coord[0], coord[1], radiuskm)
        capitalQuakes = []
        for i in result['features']:
            try:
                i['properties']['mag'] < 0.0
                capitalQuakes.append(i)
            except:
                break
        if capitalQuakes:
            allQuakes[loc] = capitalQuakes
    minMaxNPrint(allQuakes, radiuskm)


"""
implement sleep time bewteen request.get pulls
use locally stored files rather than fetching every time
"""


# this a generator function look at yield keyword!
def getMercalliIntensity():
    url = "https://en.wikipedia.org/wiki/Richter_magnitude_scale"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    intensity = {}
    tables = soup.find_all('table', {'class': 'wikitable'})
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            cols_trimed = [col.text.replace('\n', '') for col in cols]
            yield cols_trimed


def pretty_print_mercalli_intensity(data_iterator):
    header = ['Magnitude',
              'Description',
              'Mercalli',
              'intensity',
              'Average earthquake effects	Average frequency of occurrence globally (estimated)'
              ]
    print("\t|\t".join(header))
    for row in data_iterator:
        print("\t|\t".join(row))


def main():  # call function

    printQuakes("2021-01-01", "2021-02-05", 0)
    printQuakesByLatLong("2020-01-01", "2022-02-05", -33.70837, 178.52451, 100)
    shortCap = getStateCapitals("https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States")
    capitals = getLatLongDict('capitals', shortCap)
    printUSQuakeExtremes(capitals, "2020-01-01", "2022-01-01", 50)


pretty_print_mercalli_intensity(getMercalliIntensity())
