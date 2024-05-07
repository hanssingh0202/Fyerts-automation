from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
with open('access.txt','r') as a:
    access_token=a.read()
client_id = '3QYQX7SV2R-100'


fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")



def fetchOHLC(ticker,interval,duration):
  
    instrument = ticker
    data = {"symbol":instrument,"resolution":interval,"date_format":"1","range_from":dt.date.today()-dt.timedelta(duration),"range_to":dt.date.today(),"cont_flag":"1"}
    sdata=fyers.history(data)
    sdata=pd.DataFrame(sdata['candles'])
    sdata.columns=['date','open','high','low','close','volume']
    sdata['date']=pd.to_datetime(sdata['date'], unit='s')
    sdata.date=(sdata.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
    sdata['date'] = sdata['date'].dt.tz_localize(None)
    sdata=sdata.set_index('date')
    return sdata

ticker='NSE:NIFTYBANK-INDEX'
data=fetchOHLC(ticker,'1',60)
print(data)

data.to_csv('niftybankkk.csv')