from flask import Flask, jsonify, request
import sys
import pandas as pd
import os
import json
from time1 import get_time
from date import get_date
import etk_stock
import etk_webcheck

etk_apiserver = Flask(__name__)


# If the command line comes with the first argument 'public' it will set this global variable to publish the api_server
is_public = False

if len(sys.argv) > 1 and sys.argv[1] == 'public':
    is_public = True




def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

import socket

def get_host_ip():
    try:
        # Connect to a remote server (e.g., Google DNS server)
        # This won't send any data but will help determine the local IP address.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip_address = sock.getsockname()[0]
        sock.close()
    except Exception as e:
        print("Error:", e)
        ip_address = "Unknown"
    return ip_address




# ETK SERVER API ENDPOINTS 
# ------------------------
@etk_apiserver.route('/')
def hello_world():
    return '¡Hola, mundo!'

@etk_apiserver.route('/date')
def date():
    print('API Server>> La fecha de hoy es: ')
    return get_date()

@etk_apiserver.route('/time')
def time():
    print('API Server>> La hora local es: ')
    return get_time()


@etk_apiserver.route('/etk_finance/get_tickers')
def etk_get_tickers():
    print('API Server get_tickers...')
    STOP_COUNT = 100
    # Get the query parameters from the request
    exchange = request.args.get('exchange')
    print('API Server: ',exchange)

    # Call the etk_finance function with the query parameters
    myData = etk_stock.etk_finance('output_plus.xlsx')

    # Get the ticker lists from the URLs
    nyse_tickers_list = myData.get_tickers(exchange)
    nyse_tickers_df = pd.DataFrame(nyse_tickers_list, columns=['Ticker', 'Ticker Name', 'Exchange'])

    return jsonify(nyse_tickers_list), 200

# Define the API endpoint for getting the current stock price
@etk_apiserver.route('/etk_finance/get_stock_currentprice', methods=['GET'])
def get_stock_currentprice():
    print('API Server: Running get_stock_currentprice()')
    # Get the symbol and exchange parameters from the query string
    symbol = request.args.get('symbol')
    exchange = request.args.get('exchange')

    # Call the etk_finance function with the query parameters
    myData = etk_stock.etk_finance('output_plus.xlsx', username='oariasz', password='Megatrends1')
    
    # Get the symbol current stock price
    df_prices = myData.get_current_stock_price(symbol, exchange)
    if df_prices is not None:
        return str(df_prices.iloc[0]['close']), 200
    else:    
        return 'None', 200

# Define the API endpoint for getting historical stock prices
@etk_apiserver.route('/etk_finance/get_hist_prices', methods=['GET'])
def etk_get_hist():
    # Get the symbol, exchange, start_date, and end_date parameters from the query string
    symbol = request.args.get('symbol')
    exchange = request.args.get('exchange')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Call the etk_finance function with the query parameters
    myData = etk_stock.etk_finance('output_plus.xlsx', username='oariasz72', password='Megatrends1')

    if start_date == None:
        print('etk_api_server: start_date not specified')
        return
    if end_date == None:
        end_date = myData.get_todays_date

    print('ETK API Server: get_hist_prices')
    print('ETK API Server: ', symbol)
    print('ETK API Server: ', exchange)
    print('ETK API Server: ', start_date)
    print('ETK API Server: ', end_date)
    
    df_prices = myData.get_stock_data_daily_interval(symbol, exchange, start_date, end_date)
    # Remove datetime column as an index
    df_prices = df_prices.reset_index()
    # convert the datetime column to a text column
    df_prices['datetime'] = df_prices['datetime'].dt.strftime('%Y-%m-%d')
    print(df_prices)
    print(df_prices.shape)
    print(df_prices.dtypes)
    
    # df_prices.drop(['datetime'], axis=1)
    print(df_prices)
    if df_prices is not None:
        print(f'Stock {symbol} prices from {start_date} to {end_date}:')
        print (df_prices)
        list_price = df_prices.values.tolist()
        json_string = df_prices.to_json()
        
    # return json.dumps(list_price), 200
    return df_prices.to_json(), 200



# ------------------------------------------
#   M A I N   ETK API SERVER
# ------------------------------------------
if __name__ == '__main__':
    clear_screen()
    print('Starting Estratek API server...')
    host_ip = get_host_ip()
    etklab_ip = '185.211.4.151'
    host_ip = etklab_ip
    
    if is_public:
        print('The API Seerver is public on the address: ', host_ip)
        print(' ')
        etk_apiserver.run(host=host_ip, port=5000)
    else:
        print(' ')
        etk_apiserver.run()





