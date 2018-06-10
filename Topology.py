import Spouts
import json
import sys
from pprint import pprint
import datetime
import time
import trends
from geopy import geocoders
cities = {}
with open('iata.json') as f:
    iata_data = json.load(f)
city_iata = {v.lower(): k for k, v in iata_data.iteritems()}
trendingMatrix = trends.trending()
gn = geocoders.Nominatim()

def city_to_iata(city):
    if city in city_iata:
        return (city_iata[city],True)
    else:
        print "Do not have iata information of " + city
        return (city,False)

def iata_to_city(iata):
    if iata in iata_data:
        return (iata_data[iata],True)
    else:
        print "Do not have iata information of " + iata
        return (iata_data,False)

def CityDetails():
    attractionDict = {}
    city = raw_input("What is the city you want to know more about?\n")
    longitude = gn.geocode(city).raw["lon"]
    latitude = gn.geocode(city).raw["lat"]
    gattractions = Spouts.GoogleCitySpout(longitude,latitude)
    for gattraction in gattractions:
        attractionDict[gattraction["name"]]={"short_description":"","latitude":gattraction["geometry"]["location"]["lat"],"longitude":gattraction["geometry"]["location"]["lng"]}
    attractions = Spouts.CitySpout(city)
    for attraction in attractions:
        attractionDict[attraction["title"]]={"short_description":attraction["details"]["short_description"],"longitude":attraction["location"]["longitude"],"latitude":attraction["location"]["latitude"]}
    pprint(attractionDict)
    return attractionDict

def user():
    # Basic Input
    duration = raw_input("How long is your trip? (days)\n")
    budget = raw_input("Your budget for your trip?\n")
    origin = raw_input("Which airport to start from?\n")

    # Overview Information
    print "These are the top 10 searched countries in Google"
    for num in range(10):
        print trendingMatrix[num][0]

    flights = Spouts.InspirationFlightSpout(origin,duration,str(int(budget)/3))
    for flight in flights:
        iata = flight["destination"]
        city = iata_to_city(iata)
        if city[1] is True:
            flight["destination_city"] = city[0]
    print "Here are some flights information"
    pprint(flights)

    while True:
        CityDetails()
        choice = raw_input("Want to know more? Y or N\n")
        if choice == 'N' or choice == 'n':
            break
        elif choice == 'Y' or choice == 'y':
            pass
        else:
            print "invalid input"
            sys.exit()


    destination = raw_input('What is your destination?\n')
    destination = destination.lower()

    start = raw_input("Start time? Year-Month-Day\n")
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    date += datetime.timedelta(days=int(duration))
    checkout =  date.strftime('%Y-%m-%d')
    des_res = city_to_iata(destination)
    if des_res[1] == True:
        des_airport = des_res[0]
    else:
        print "NO iata information"
        sys.exit()
    fares = Spouts.LowFareSpout(origin,des_airport,start,checkout)
    print "fares"
    pprint(fares)

    #yy = raw_input("Press any key to show hotels\n")
    hotels = Spouts.HotelSpout(des_airport,start,checkout)

    pprint(hotels)


if __name__ == '__main__':
    print user()
