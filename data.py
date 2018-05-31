import json
from pprint import pprint
import datetime
# airportdic = {}
# with open('airports.json') as f:
#     data = json.load(f)
#     for airport in data:
#         airportdic[airport] = data[airport]["city"]
# with open('data.json', 'w') as outfile:
#     json.dump(airportdic, outfile)

date = datetime.datetime.strptime('2016-01-28', '%Y-%m-%d')
date += datetime.timedelta(days=7)
print date.strftime('%Y-%m-%d')
