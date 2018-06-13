# -- coding: utf-8 --
import json
import Topology
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
cities = {}
with open('iata.json') as f:
    iata_data = json.load(f)
city_iata = {v.lower(): k for k, v in iata_data.iteritems()}
trendingMatrix = trends.trending()
gn = geocoders.Nominatim()
top_fifty=[]
for num in range(50):
    top_fifty.append(trendingMatrix[num][0])
trend_score=0

def city_to_iata(city):
    if city in city_iata:
        return (city_iata[city],True)
    else:
        print "Do not have iata information of " + city
        return (city,False)

with open('plan_data.json', 'r') as fp:
    data = json.load(fp)

score = data["score"]
email = data["user_email"]
duration = data["duration"]
budget = data["budget"]
origin = data["origin"]
destination = data["destination"]
start = data["start"]
date = datetime.datetime.strptime(start, '%Y-%m-%d')
date += datetime.timedelta(days=int(duration))
checkout =  date.strftime('%Y-%m-%d')
citylongitude = gn.geocode(destination).raw["lon"]
citylatitude = gn.geocode(destination).raw["lat"]

temperature,wind_speed=pl.get_temp(int(duration), destination)
if destination in top_fifty:
    trend_score=50-top_fifty.index(destination)

des_res = city_to_iata(destination)
if des_res[1] == True:
    des_airport = des_res[0]
    # print des_airport
else:
    print "NO iata information"
    sys.exit()

fares = Spouts.LowFareSpout(origin,des_airport,start,checkout)
hotels = Spouts.HotelSpout(des_airport,start,checkout)
poi = Topology.destination_Details(destination)
lowest_cost = float(hotels[0].get('total_price').get('amount')) + float(fares[0].get('fare').get('total_price'))
newscore=pl.rate(temperature,wind_speed,(lowest_cost),int(budget),trend_score)
print "new score is: "
print newscore
if abs(newscore-score)>10:
    plan_to_mail=pl.make_plan_new(int(duration),poi,fares,hotels,0)
    hotel_short = {"name":hotels[0]["property_name"],"address": hotels[0]["address"],"price":hotels[0]["total_price"]}
    mail = {"score":newscore,"user_email":email,"cost":lowest_cost,"plan":plan_to_mail,"flight_detail":fares[0],"hotel_detail":hotel_short}
    sp.sendPlan(mail)
    user_input = {"score":newscore,"user_email":email,"duration":duration,"budget":budget,"origin":origin,"destination":destination,"start":start}
    with open('plan_data.json', 'w') as fp:
        json.dump(user_input, fp)
