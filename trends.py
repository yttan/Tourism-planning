import datetime
import pandas as pd
from pytrends.request import TrendReq

def trending():
    mydate =  (datetime.date.today()-datetime.timedelta(3*365/12)).strftime("%Y%m")
    pytrend = TrendReq()
    top_charts_df = pytrend.top_charts(cid='countries', date= str(mydate),geo='US')
    column = ['title']
    trending  = top_charts_df[column]
    trendingMatrix = trending.as_matrix()
    return trendingMatrix

if __name__ == '__main__':
    trending()
