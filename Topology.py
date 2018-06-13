# -- coding: utf-8 --
import send_plan as sp
import weather_plan as pl
import Spouts
import json
import sys
from pprint import pprint
import datetime
import time
import trends
from geopy import geocoders
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
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
        if '\u' in gattractions:
            break
        else:
            attractionDict[gattraction["name"]]={"short_description":"","latitude":gattraction["geometry"]["location"]["lat"],"longitude":gattraction["geometry"]["location"]["lng"]}
    attractions = Spouts.CitySpout(city)
    for attraction in attractions:
        attractionDict[attraction["title"]]={"short_description":attraction["details"]["short_description"],"longitude":attraction["location"]["longitude"],"latitude":attraction["location"]["latitude"]}
    pprint(attractionDict)
    return attractionDict

def destination_Details(city):
    attractionDict = {}
    longitude = gn.geocode(city).raw["lon"]
    latitude = gn.geocode(city).raw["lat"]
    gattractions = Spouts.GoogleCitySpout(longitude,latitude)
    for gattraction in gattractions:
        if '\u' in gattractions:
            break
        else:
            attractionDict[gattraction["name"]]={"short_description":"","latitude":gattraction["geometry"]["location"]["lat"],"longitude":gattraction["geometry"]["location"]["lng"]}
    attractions = Spouts.CitySpout(city)
    for attraction in attractions:
        attractionDict[attraction["title"]]={"short_description":attraction["details"]["short_description"],"longitude":attraction["location"]["longitude"],"latitude":attraction["location"]["latitude"]}
    #pprint(attractionDict)
    return attractionDict

def topRestaurants(longitude,latitude):
    restaurants = Spouts.GoogleRestaurant(longitude,latitude)
    restaurantsDict = {}
    i=1
    for restaurant in restaurants:
        restaurantsDict[i] = {"name":restaurant["name"],"latitude":restaurant["geometry"]["location"]["lat"],"longitude":restaurant["geometry"]["location"]["lng"]}
        i+=1
    num = len(restaurantsDict)
    if num <= 10:
        return restaurantsDict
    else:
        newDict = {}
        for j in range(1,11):
            newDict[j] = restaurantsDict[j]
        return newDict

def user():
    # Basic Input
    top_fifty=[]
    print "Welcome to the Tourism Planning System!"
    print "Please following the instructions to input your requirements."
    duration = raw_input("How long is your trip? (days)\n")
    budget = raw_input("Your budget($) for your trip?\n")
    origin = raw_input("Which airport are you going to start from?\n")

    # Overview Information
    print "Here are the top 10 hot countries for tourism searched in Google"
    for num in range(10):
        print trendingMatrix[num][0]
    for num in range(50):
        top_fifty.append(trendingMatrix[num][0])
    keyforwait = raw_input("Input any key to show some inspiration flights information\n")
    flights = Spouts.InspirationFlightSpout(origin,duration,str(int(budget)/3))
    for flight in flights:
        iata = flight["destination"]
        city = iata_to_city(iata)
        if city[1] is True:
            flight["destination_city"] = city[0]
    pprint(flights)

    while True:
        CityDetails()
        choice = raw_input("Want to see information about another city? Y or N\n")
        if choice == 'N' or choice == 'n':
            break
        elif choice == 'Y' or choice == 'y':
            pass
        else:
            print "invalid input"
            sys.exit()


    destination = raw_input('What is your destination city?\n')
    destination = destination.lower()
    poi =destination_Details(destination)
    trend_score=0
    if destination in top_fifty:
        trend_score=50-top_fifty.index(destination)

    start = raw_input("Start time? Year-Month-Day\n")
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    date += datetime.timedelta(days=int(duration))
    checkout =  date.strftime('%Y-%m-%d')
    print'You are now planning going to',destination,'for',duration,'days'
    print 'The trip will start on',start,'end on',checkout

    citylongitude = gn.geocode(destination).raw["lon"]
    citylatitude = gn.geocode(destination).raw["lat"]
    print 'Here are the top restaurants in ' + destination
    rests = topRestaurants(citylongitude, citylatitude)
    for i in range(1, len(rests)+1):
        print "top " + str(i)
        print rests[i]["name"]
    print 'Here shows some weather information of your trip:'
    # print duration
    temperature,wind_speed=pl.get_temp(int(duration), destination)

    des_res = city_to_iata(destination)
    if des_res[1] == True:
        des_airport = des_res[0]
        # print des_airport
    else:
        print "NO iata information"
        sys.exit()
    fares = Spouts.LowFareSpout(origin,des_airport,start,checkout)
    print 'Here shows some flight prices:'
    for i in range(0,len(fares)):
        if i<20:
            print 'flight plan',i
            # print fares[i].get('itineraries').get('inbound').get('duration')
            # print fares[i].get('itineraries').get('inbound').get('flights').get('departs_at')
            # print fares[i].get('itineraries').get('inbound').get('flights').get('arrives_at')
            # print fares[i].get('itineraries').get('outbound').get('duration')
            # print fares[i].get('itineraries').get('outbound').get('flights').get('departs_at')
            # print fares[i].get('itineraries').get('outbound').get('flights').get('arrives_at')
            print(fares[i].get('fare').get('total_price'))

    # print "fares"
    # pprint(fares[6])
    # pprint(fares[0].get('fare').get('total_price'))
    #yy = raw_input("Press any key to show hotels\n")
    hotels = Spouts.HotelSpout(des_airport,start,checkout)
    for i in range(0,len(hotels)):
        if i<10:
        # pprint(hotels[0])
            print 'Here is some hotel reccomendation:'
            print 'Hotel No.'+str(i+1)
            print hotels[i].get('property_name')
            print hotels[i].get('address').get('line1')
            print 'total Prices for',duration,'days:',hotels[i].get('total_price').get('amount'),'$'
            # pprint(hotels)

        # print hotels[1].get('total_price').get('amount')
        # print hotels[2].get('total_price').get('amount')
        # print hotels[3].get('total_price').get('amount')

    print 'Do you want the system to help you making the tourism plan? Input 1 for yes: '
    plan=input()
    if plan!=1:
        return
    # print lowest_cost
    # print budget
    plan_num=0
    lowest_cost = 0
    score = 0
    while(1):
        lowest_cost = float(hotels[plan_num].get('total_price').get('amount')) + float(fares[plan_num].get('fare').get('total_price'))
        score=pl.rate(temperature,wind_speed,(lowest_cost),int(budget),trend_score)
        print "Now showing the Plan number",plan_num+1
        print 'Total score of this plan is',score
        # print poi
        plan_to_mail=pl.make_plan(int(duration),poi,fares,hotels,plan_num)
        print 'Input 1 see the previous plan, input 2 to see next plan,Input 3 to select this plan.'
        pl_num=input()
        if pl_num==1:
            plan_num=plan_num-1
        elif pl_num==2:
            plan_num=plan_num+1
        else:
            break

    while (1):
        print "Do you want to see the detail of your flight or hotel information?"
        print "Input 1 to see the flight information, 2 for hotel information, and any key else to send your plan"
        detailed=input()
        if detailed==1:
            pprint(fares[plan_num])
        elif detailed==2:
            pprint(hotels[plan_num])
        else:
            break

    print('please input your email address so we can see the plan to you and contact you when big changes happen:')
    address=raw_input()

    hotel_short = {"name":hotels[plan_num]["property_name"],"address": hotels[plan_num]["address"],"price":hotels[plan_num]["total_price"]}
    mail = {"score":score,"user_email":address,"cost":lowest_cost,"plan":plan_to_mail,"flight_detail":fares[plan_num],"hotel_detail":hotel_short}
    user_input = {"score":score,"user_email":address,"duration":duration,"budget":budget,"origin":origin,"destination":destination,"start":start}
    sp.sendPlan(mail)
    print "Plan complete! Thanks for using our system!"
    print "We will notify you by emails if there is any big changes in your plan. "
    print "Wish your a wonderful trip!"

    with open('plan_data.json', 'w') as fp:
        json.dump(user_input, fp)




if __name__ == '__main__':
    user()
