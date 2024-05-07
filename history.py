from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt
with open('access.txt','r') as a:
    access_token=a.read()
client_id = '3QYQX7SV2R-100'

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")




data = {
    "symbol":"NSE:RELIANCE-EQ",
    "resolution":"1",
    "date_format":"1",
    "range_from":"2024-04-11",
    "range_to":"2024-04-12",
    "cont_flag":"1"
}

response = fyers.history(data=data)
#print(response)
data=response['candles']
df=pd.DataFrame(data)


df.columns=['date','open','high','low','close','volume']
df['date']=pd.to_datetime(df['date'], unit='s')

df.date=(df.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))

df['date'] = df['date'].dt.tz_localize(None)
df=df.set_index('date')
print(df)
df.to_csv('data.csv')
print(dt.datetime.now())






