from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
with open('access.txt','r') as a:
    access_token=a.read()
client_id = '3QYQX7SV2R-100'


fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")







def gethistory(symbol1,type,duration):
    symbol="NSE:"+symbol1+"-"+type
    start=dt.date.today()-dt.timedelta(duration)
    end=dt.date.today()-dt.timedelta()
    sdata=pd.DataFrame()
    while start <= end:
        end2=start+dt.timedelta(60)
        data = {"symbol":symbol,"resolution":"1","date_format":"1","range_from":start,"range_to":end2,"cont_flag":"1"}
        s=fyers.history(data)
        s=pd.DataFrame(s['candles'])
        sdata=pd.concat([sdata,s],ignore_index=True)
        start=end2+dt.timedelta(1)
    sdata.columns=['date','open','high','low','close','volume']
    sdata["date"]=pd.to_datetime(sdata['date'], unit='s')
    sdata.date=(sdata.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
    sdata['date'] = sdata['date'].dt.tz_localize(None)
    sdata=sdata.set_index('date')
    return sdata

data=gethistory('TATAMOTORS','EQ',500)
print(data)
data.to_csv('niftybankk.csv')