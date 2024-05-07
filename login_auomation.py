
from fyers_apiv3 import fyersModel
#All information 
client_id = '3QYQX7SV2R-100'
secret_key = '2MSTSKFUZB'
redirect_uri ='https://fyers.in/products/api/'
user_name ='YH03438'

totp_key='HR6LFQJNMJ5FIHWZCUUK6GUQ2QJROFVL'
#fyers pin
pin1 ="0"
pin2 = "2"
pin3 = "0"
pin4 = "2"

response_type = "code"  
state = "sample_state"


session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)


response = session.generate_authcode()


print(response)

link = response

#Selenium part start


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pyotp as tp


driver = webdriver.Chrome()



driver.get(link)

#client id page automation

time.sleep(1)
login_with_client_id_x_path='//*[@id="login_client_id"]'
elem = driver.find_element(By.XPATH, login_with_client_id_x_path)
elem.click()
time.sleep(1)
client_id_input_x_path='//*[@id="fy_client_id"]'
elem2 = driver.find_element(By.XPATH, client_id_input_x_path)
elem2.send_keys("YH03438")
elem2.send_keys(Keys.RETURN)
time.sleep(1)

t=tp.TOTP(totp_key).now()

#totp page

driver.find_element(By.XPATH, '//*[@id="first"]').send_keys(t[0])
driver.find_element(By.XPATH, '//*[@id="second"]').send_keys(t[1])
driver.find_element(By.XPATH, '//*[@id="third"]').send_keys(t[2])
driver.find_element(By.XPATH, '//*[@id="fourth"]').send_keys(t[3])
driver.find_element(By.XPATH, '//*[@id="fifth"]').send_keys(t[4])
driver.find_element(By.XPATH, '//*[@id="sixth"]').send_keys(t[5])

driver.find_element(By.XPATH, '//*[@id="confirmOtpSubmit"]').click() 
time.sleep(1)

#fyers pin page

driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"first").send_keys(pin1)
driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"second").send_keys(pin2)
driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"third").send_keys(pin3)
driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"fourth").send_keys(pin4)

driver.find_element(By.XPATH,'//*[@id="verifyPinSubmit"]').click()
time.sleep(10)


newurl = driver.current_url
print(newurl)
auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
print(auth_code)




driver.close()
#access token part

from fyers_apiv3 import fyersModel

response_type = "code" 
grant_type = "authorization_code"  


session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

session.set_token(auth_code)

response = session.generate_token()

print(response)

access_token=response['access_token']
with open('access.txt','w') as k:
    k.write(access_token)

