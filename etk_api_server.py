from flask import Flask, jsonify, request
import requests
from time1 import get_time
from date import get_date
import etk_stock
import pandas as pd


etk_apiserver = Flask(__name__)


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
    STOP_COUNT = 10
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
    myData = etk_stock.etk_finance('output_plus.xlsx')
    
    # Get the symbol current stock price
    df_prices = myData.get_current_stock_price(symbol, exchange)
    print(df_prices)
    if df_prices is not None:
       print('Resultados')
       print(df_prices)
    return jsonify(df_prices), 200

# Define the API endpoint for getting historical stock prices
@etk_apiserver.route('/etk_finance/get_hist', methods=['GET'])
def etk_get_hist():
    # Get the symbol, exchange, start_date, and end_date parameters from the query string
    symbol = request.args.get('symbol')
    exchange = request.args.get('exchange')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Call the etk_finance function with the query parameters
    myData = etk_stock.etk_finance('output_plus.xlsx')
    

    if start_date == None:
        print('api_client: start_date not specified')
        return
    if end_date == None:
        end_date = myData.get_todays_date

    df_prices = myData.get_stock_data_daily_interval(symbol, exchange, start_date, end_date)
    if df_prices is not None:
        print(f'Stock {symbol} prices from {start_date} to {end_date}')
        print(df_prices), 200    
        
    return jsonify(df_prices)



# ------------------------------------------
#   M A I N
# ------------------------------------------
if __name__ == '__main__':
    print('Starting Estratek API server...')
    etk_apiserver.run()






