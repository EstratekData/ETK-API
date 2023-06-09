from flask import Flask, jsonify, request
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


@etk_apiserver.route('/etk_finance')
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

    return jsonify(nyse_tickers_list)

if __name__ == '__main__':
    print('Starting Estratek API server...')
    etk_apiserver.run()




'''
# Anterior version de etk_get_tickers

@etk_apiserver.route('/etk_finance')
def etk_get_tickers():
    STOP_COUNT = 10
    myData = etk_stock.etk_finance('output_plus.xlsx') 

    # 1. Get the ticker lists from the URLs
    nyse_tickers_list = myData.get_tickers('NYSE')
    print ('NYSE Tickers List')
    nyse_tickers_df = pd.DataFrame(nyse_tickers_list, columns=['Ticker', 'Ticker Name', 'Exchange'])
    print(nyse_tickers_list)
    return jsonify(nyse_tickers_list)

'''