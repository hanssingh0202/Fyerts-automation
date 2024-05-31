from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
import datetime as dt

with open('access.txt','r') as a:
    access_token = a.read()

client_id = '3QYQX7SV2R-100'

# Define a variable to store the last traded price
last_price = None

# Define ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def onmessage(message):
    global last_price
    
    # Get the current timestamp
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Extract the last traded price from the message
    ltp = message.get('ltp', None)

    if ltp is not None:
        # Check if this is the first price received
        if last_price is None:
            last_price = ltp
            return
        
        # Calculate the percentage change
        price_change = ((ltp - last_price) / last_price) * 100
        # Print the received message
        print("Message received:", message)
        # Print the calculated percentage change
        print("Price Change:", price_change)

        # Check if the absolute value of the percentage change is greater than or equal to 0.1%
        if abs(price_change) >= 0.1:
            if price_change > 0:
                # If the price increased by more than 0.1%, print a buy signal in green
                print(f"{GREEN}Signal: BUY, Price: {ltp}, Time: {current_time}{RESET}")
            else:
                # If the price decreased by more than 0.1%, print a sell signal in red
                print(f"{RED}Signal: SELL, Price: {ltp}, Time: {current_time}{RESET}")

        # Update the last traded price
        last_price = ltp

def onerror(message):
    """
    Callback function to handle WebSocket errors.

    Parameters:
        message (dict): The error message received from the WebSocket.
    """
    print("Error:", message)

def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)

def onopen():
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.
    """
    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Subscribe to the specified symbols and data type
    symbols = ['NSE:INFY-EQ']
    fyers.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()

# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=access_token,       # Access token in the format "appid:accesstoken"
    log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=False,                  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,             # Save response in a log file instead of printing it.
    reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
    on_connect=onopen,               # Callback function to subscribe to data upon connection.
    on_close=onclose,                # Callback function to handle WebSocket connection close events.
    on_error=onerror,                # Callback function to handle WebSocket errors.
    on_message=onmessage             # Callback function to handle incoming messages from the WebSocket.
)
fyers.connect()
