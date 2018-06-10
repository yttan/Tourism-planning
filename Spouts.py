import requests
import sys
from pprint import pprint

key = '--------------'
MAP_KEY = "------------------"

def InspirationFlightSpout(origin,duration,price):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin='+origin+'&apikey='+key+'&duration='+duration+'&max_price='+price)
    data = r.json()
    return data['results']

def FlightSpout2(origin):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin='+origin+'&apikey='+key)
    data = r.json()
    return data['results']

def HotelSpout(airport,checkin,checkout):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?location='+airport+'&apikey='+key+'&check_in='+checkin+'&check_out='+checkout)
    data = r.json()
    return data["results"]

def CitySpout(city):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey='+key+'&city_name='+city)
    data = r.json()
    error = 'error'
    if error in data:
        print 'HTTP request error'
        return data["error"]
    else:
        return data["points_of_interest"]

def GoogleCitySpout(longitude,latitude):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+latitude+','+longitude+'&radius=40000&type=point_of_interest&key='+MAP_KEY
    r = requests.get(url)
    data = r.json()
    #pprint(data)
    if data["status"] == u'ZERO_RESULTS':
        return []
    elif data["status"] == u'UNKNOWN_ERROR':
        return []
    else:
        return data['results']

def LowFareSpout(origin,destination,departure,return_date):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey='+key+'&origin='+origin+'&destination='+destination+'&departure_date='+departure+'&return_date='+return_date)
    data = r.json()
    return data["results"]
