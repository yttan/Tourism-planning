import datetime
import pandas as pd
from pytrends.request import TrendReq

date =  datetime.datetime.now().strftime("%Y%m")
pytrend = TrendReq()
top_charts_df = pytrend.top_charts(cid='countries', date=201712,geo='US')
column = ['title']
trending  = top_charts_df[column]
print trending
