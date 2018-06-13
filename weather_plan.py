# -- coding: utf-8 --
import sys

import json
import urllib2

import webbrowser as web
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
# key = 'b6158bbe2535450a3a8632c387f09bc7'


def get_json_weather(cityname):
    # print 'which city?'
    # url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=b6158bbe2535450a3a8632c387f09bc7'
    url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + str(
        cityname) + '&APPID=b6158bbe2535450a3a8632c387f09bc7'
    # url='http://api.openweathermap.org/data/2.5/forecast?q=Beijing&mode=json&APPID=b6158bbe2535450a3a8632c387f09bc7'
    html = urllib2.urlopen(url).read()
    return html


def get_temp(days,cityname):
    data = get_json_weather(cityname)
    hjson = json.loads(data)
    # pprint(hjson)
    # pprint(hjson['city'])
    # pprint(hjson['list'][1])
    if days > 5:
        daynum = 5
    else:
        daynum = days
    temperature = []
    wind_sp = []
    for i in range(0, daynum):
        print 'The weather of day ',i+1,( hjson.get('list')[1+8*i].get('weather')[0].get('description'))
        print 'The temperature of day ', i + 1, 'is', (int(hjson['list'][1+8*i].get('main').get('temp') - 273.5)), 'C'
        print 'The Wind speed of day ', i + 1, 'is', ((hjson['list'][1+8*i].get('wind').get('speed')))
        temperature.append((int(hjson['list'][1+8*i].get('main').get('temp') - 273.5)))
        wind_sp.append(hjson['list'][1+8*i].get('wind').get('speed'))
    return temperature, wind_sp


def rate(temp,wind_s,cost,total_budget,trend_score):
    score=0
    aver_wd = 0
    aver_tp = 0

    # trend=50-% budget:200*2
    for i in range(0,len(temp)):
        tp=temp[i]
        aver_tp=tp+aver_tp
        if abs(tp-20)<5:
            score+=100
        elif abs(tp-20)<8:
            score+=80
        elif abs(tp-20)<11:
            score+=50
        elif abs(tp-20)<15:
            score+=20
        else :
            score+=0
    for i in range(0,len(wind_s)):
        ws=wind_s[i]
        aver_wd=aver_wd+ws
        if ws<3:
            score+=100
        elif ws<5:
            score+=80
        elif ws<6:
            score+=50
        elif ws<7:
            score+=20
        else :
            score+=0
    score=score/len(temp)
    score=score+200-2*cost/total_budget/0.6
    score=score+trend_score
    # print 'Temperature',aver_tp/3
    # print 'Wind_speed',aver_wd/3
    return score


# tprt, wdsd = get_temp(days)
# print (tprt,wdsd)
# final_score=rate(tprt,wdsd)
# print final_score





def open_map(url):
    web.open_new_tab(url)
    print 'run_to_use_default_browser_open_url  open url ending ....'



# open_map('https://www.google.com/maps/dir/31.06250,+118.7780/32.0625,118.778/33.06250,+118.7780/@32.0207752,117.5535613')
def move(lst, k):
    return lst[k:] + lst[:k]

def find_url(x, y):
    string = 'https://www.google.com/maps/dir/'
    # print string
    for i in range(0, len(x)):
        if x[i] != 0:
            string = string + str(x[i]) + ',' + str(y[i]) + '/'
    string = string + '@' + str(x[0]) + ',' + str(y[0]) + '/'
    # print string
    return string

def make_plan(days,sh,flight,hotel,plan_num):
    print "Now planning a",days,'Day tourism for you:'
    print "Flight_total_cost:",flight[plan_num%len(flight)].get('fare').get('total_price')
    print 'Hotel total cost:',hotel[plan_num%len(hotel)].get('total_price').get('amount')
    mail_plan=[]
    name = []
    x = []
    y = []
    description = []
    for i in range(0, len(sh)):
        # image.append(sh[i].get('main_image'))
        # name.append(sh[i].get('title'))
        # map.append(sh[i].get('location').get('google_maps_link'))
        # description.append(sh[i].get('details').get('short_description'))
        # x.append(sh[i].get('location').get('latitude'))
        # y.append(sh[i].get('location').get('longitude'))
        name.append(sh.keys()[i])
        description.append(sh.get(sh.keys()[i]).get('short_description'))
        x.append(sh.get(sh.keys()[i]).get('latitude'))
        y.append(sh.get(sh.keys()[i]).get('longitude'))
    name=move(name,plan_num*2)
    description=move(description,plan_num*2)
    x=move(x,plan_num*2)
    y=move(y,plan_num*2)

        # pprint(sh[0].get('location'))
    # print len(sh)
    if len(sh) < days:
        for i in range(len(sh), days):
            name.append('shopping')
            x.append(0)
            y.append(0)
        for i in range(0, days):
            print "Day", i + 1
            if i == 0:
                print 'Destination Airport Arrived'
            print name[i]
            if (x[i] != 0):
                print(description[i])
                # print image[i]
                # print map[i]
                # print (x[i],y[i])

    elif len(sh) >= days:
        for i in range(0, days):
            print "Day", i + 1
            if i == 0:
                print 'Destination Airport Arrived'
            mail_plan.append('Day')
            mail_plan[i] += str(i + 1) + '\n'
            for j in range(0, len(sh)):
                if j % days == i:
                    print name[j]
                    print(description[j])
                    mail_plan[i]+=(str(name[j])+' '+str(description[j])+'\n')

                    # print image[j]
                    # print map[j]
                    # print (x[j], y[j])
    mapweb=find_url(x,y)
    print 'Plan accomplished'

    print 'Input 1 to show the route on google map:'
    a = input()
    if a == 1:
        open_map(mapweb)

    return mail_plan

# def main():
#
#     tprt, wdsd = get_temp(days)
#     # print (tprt, wdsd)
#     final_score = rate(tprt, wdsd)
#     print 'Total score of this plan is ',final_score
#     place , x, y = make_plan(days,sh)
#     mapweb = find_url(x, y)

#
# main()


def make_plan_new(days,sh,flight,hotel,plan_num):
    mail_plan=[]
    name = []
    x = []
    y = []
    description = []
    for i in range(0, len(sh)):
        # image.append(sh[i].get('main_image'))
        # name.append(sh[i].get('title'))
        # map.append(sh[i].get('location').get('google_maps_link'))
        # description.append(sh[i].get('details').get('short_description'))
        # x.append(sh[i].get('location').get('latitude'))
        # y.append(sh[i].get('location').get('longitude'))
        name.append(sh.keys()[i])
        description.append(sh.get(sh.keys()[i]).get('short_description'))
        x.append(sh.get(sh.keys()[i]).get('latitude'))
        y.append(sh.get(sh.keys()[i]).get('longitude'))
    name=move(name,plan_num*2)
    description=move(description,plan_num*2)
    x=move(x,plan_num*2)
    y=move(y,plan_num*2)

        # pprint(sh[0].get('location'))
    # print len(sh)
    if len(sh) < days:
        for i in range(len(sh), days):
            name.append('shopping')
            x.append(0)
            y.append(0)

    elif len(sh) >= days:
        for i in range(0, days):
            mail_plan.append('Day')
            mail_plan[i] += str(i + 1) + '\n'
            for j in range(0, len(sh)):
                if j % days == i:
                    print name[j]
                    print(description[j])
                    mail_plan[i]+=(str(name[j])+' '+str(description[j])+'\n')

    return mail_plan
