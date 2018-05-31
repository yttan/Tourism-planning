import Spouts
import json
import sys
from pprint import pprint
import datetime
cities = {}
iata_data = None
def iata_to_city(iata):
    global iata_data
    with open('iata.json') as f:
        iata_data = json.load(f)
        if iata in iata_data:
            return (iata_data[iata],True)
        else:
            print "Do not have iata information of " + iata
            return (iata_data,False)

def CityDetails():
    city = raw_input("What is the city you want to know more about?\n")
    city = city.lower()
    if city in cities:
        attractions = Spouts.CitySpout(cities[city][0])
        with open('attractions.json', 'w') as outfile:

            json.dump(attractions, outfile)

        pprint(attractions)
    else:
        print "The city is not in database or you have a type error."

def getData():
    global cities
    while True:
        sleep(60)
        flights = FlightSpout2('LAX')
        for flight in flights:
            iata = flight["destination"]
            city = iata_to_city(iata)
            if city[1] is True:
                flight["destination_city"] = city[0]
                cities[city[0].lower()] = [city[0],iata]

def user():
    global cities
    duration = raw_input("How long is your trip? (days)\n")
    origin = raw_input("Which airport to start from?\n")
    flights = Spouts.FlightSpout(origin,duration)
    for flight in flights:
        iata = flight["destination"]
        city = iata_to_city(iata)
        if city[1] is True:
            flight["destination_city"] = city[0]
            cities[city[0].lower()] = [city[0],iata]
    #print cities
    print "Here are some flights information"
    pprint(flights)
    with open('flights.json', 'w') as outfile:
        json.dump(flights, outfile)

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
    des_city = cities[destination][0]
    des_airport = cities[destination][1]
    start = raw_input("Start time? Year-Month-Day\n")
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    date += datetime.timedelta(days=int(duration))
    checkout =  date.strftime('%Y-%m-%d')
    fares = Spouts.LowFareSpout(origin,des_airport,start,checkout)
    print "fares"
    pprint(fares)
    with open('fares.json', 'w') as outfile:
        json.dump(fares, outfile)

    yy = raw_input("Press any key to show hotels\n")
    hotels = Spouts.HotelSpout(des_airport,start,checkout)
    with open('hotels.json', 'w') as outfile:
        json.dump(hotels, outfile)
    pprint(hotels)


if __name__ == '__main__':
    user()
