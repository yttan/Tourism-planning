import requests
import sys
def FlightSpout(origin,duration):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin='+origin+'&apikey=goTs2OMgouGoi5nBhsBcpK11RWe7dDdE'+'&duration='+duration)
    data = r.json()
    return data['results']

def FlightSpout2(origin):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin='+origin+'&apikey=goTs2OMgouGoi5nBhsBcpK11RWe7dDdE')
    data = r.json()
    return data['results']

def HotelSpout(airport,checkin,checkout):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?location='+airport+'&apikey=goTs2OMgouGoi5nBhsBcpK11RWe7dDdE'+'&check_in='+checkin+'&check_out='+checkout)
    data = r.json()
    return data["results"]

def CitySpout(city):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?apikey=goTs2OMgouGoi5nBhsBcpK11RWe7dDdE'+'&city_name='+city)
    data = r.json()
    error = 'error'
    if error in data:
        print 'HTTP request error'
        return data["error"]
    else:
        return data["points_of_interest"]

def LowFareSpout(origin,destination,departure,return_date):
    r = requests.get('https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey=goTs2OMgouGoi5nBhsBcpK11RWe7dDdE&origin='+origin+'&destination='+destination+'&departure_date='+departure+'&return_date='+return_date)
    data = r.json()
    return data["results"]
