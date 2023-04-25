import json
import os
import sys
import requests
import pandas as pd
import argparse
from etk_finance.etk_stock import etk_finance
from etk_webcheck.etk_webcheck import WebCheck



api_url = 'http://localhost:5000'




def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class APIClient:
    # Method: __init__(self)   ---------------------------------------------------
    # Constructor in charge of parsing the command line arguments of api_client.py
    def __init__(self):
        # Create an argument parser with a help message
        self.parser = argparse.ArgumentParser(description='API client', 
                                              usage='python api_client.py <command> [<args>]')
        # Add arguments for the API commands and their sub-commands
        subparsers = self.parser.add_subparsers(dest='api_command')

        # etk_finance command and its sub-commands
        etk_finance_parser = subparsers.add_parser('etk_finance', help='ETK Finance API')
        etk_finance_subparsers = etk_finance_parser.add_subparsers(dest='sub_command')

        get_stock_currentprice_parser = etk_finance_subparsers.add_parser('get_stock_currentprice', 
                                                                         help='Get current stock price')
        get_stock_currentprice_parser.add_argument('symbol', help='The stock symbol')
        get_stock_currentprice_parser.add_argument('exchange', help='The stock exchange')

        get_hist_prices_parser = etk_finance_subparsers.add_parser('get_hist_prices', 
                                                                   help='Get historical stock prices')
        get_hist_prices_parser.add_argument('symbol', help='The stock symbol')
        get_hist_prices_parser.add_argument('exchange', help='The stock exchange')
        get_hist_prices_parser.add_argument('-f', '--filename', help='The filename to which the data will be saved. If not specified, the data will be printed to the console.')
        get_hist_prices_parser.add_argument('-add', action='store_true', help='If specified, the data will be appended to the file instead of overwriting it.')
        get_hist_prices_parser.add_argument('-new', action='store_true', help='If specified, a new file will be created instead of overwriting an existing file.')
        get_hist_prices_parser.add_argument('start_date', help='The start date (YYYY-MM-DD)')
        get_hist_prices_parser.add_argument('end_date', help='The end date (YYYY-MM-DD)')

        get_ticker_list_parser = etk_finance_subparsers.add_parser('get_ticker_list', 
                                                                   help='Get list of tickers')
        get_ticker_list_parser.add_argument('-f', '--output_filename', help='The output filename to which the tickers will be saved. If not specified, the tickers will be printed to the console.')
        get_ticker_list_parser.add_argument('exchange', help='The stock exchange')
        
        # webcheck command
        webcheck_parser = subparsers.add_parser('etk_webcheck', help='Web check API')
        webcheck_parser.add_argument('url', help='The URL to check')
                        
    # Method: dispatcher(self, args)   ------------------------------------
    # Method to execute the API calls depending on the parsed args provided
    def dispatcher(self, args):
        # Extract command-specific arguments
        api_command = args.api_command
        sub_command = getattr(args, 'sub_command', None)

        # Put args into readable variables
        if sub_command == 'get_stock_currentprice':
            # Extract the stock symbol and exchange for the get_stock_currentprice sub-command
            symbol = args.symbol
            exchange = args.exchange
        elif sub_command == 'get_hist_prices':
            # Extract the stock symbol, exchange, filename, add_to_file, new_file, start_date, and end_date for the get_hist_prices sub-command
            symbol = args.symbol
            exchange = args.exchange
            filename = args.filename
            add_to_file = args.add
            new_file = args.new
            start_date = args.start_date
            end_date = args.end_date
        elif sub_command == 'get_ticker_list':
            # Extract the output filename for the get_ticker_list sub-command
            output_filename = args.output_filename
        elif api_command == 'etk_webcheck':
            # Extract the URL to check for the etk_webcheck command
            url = args.url

        # Make API calls using the extracted arguments
        if api_command == 'etk_finance':
            print('ETK_FINANCEEEEEEEEEEEEEEEE')
            if sub_command == 'get_stock_currentprice':                                     # <--- get_stock_currentprice
                # Make API call to get the current stock price using symbol and exchange
                print(f"Getting current price for {symbol} on {exchange}...")
                api_etk_finance_get_stock_currentprice(symbol, exchange)

            elif sub_command == 'get_hist_prices':                                          # <--- get_hist_prices
                # Make API call to get historical stock prices using symbol, exchange, filename, add_to_file, new_file, start_date, and end_date
                print(f"Getting historical prices for {symbol} on {exchange} between {start_date} and {end_date}...")
                api_etk_finance_get_hist_prices(symbol, exchange, start_date, end_date)
                if filename:
                    print(f"Data will be saved to {filename}")
            elif sub_command == 'get_ticker_list':                                          # <--- get_ticker_list
                print('Holaaaaaaaaaaa')
                exchange = args.exchange
                # Make API call to get the list of tickers using output_filename
                print(f"Getting ticker list, output will be saved to {output_filename if output_filename else 'console'}")
                api_etk_finance_get_tickers(exchange)
            else:
                # Print help message if the sub-command is not recognized
                print(f'api_client: etk_finance subcommand {sub_command} not recognized.')
                # etk_finance_parser.print_help()
        elif api_command == 'etk_webcheck':
            # Make API call to check the URL using url
            arg_list = sys.argv[1:]
            if len(arg_list) <= 3:
                print(f"Checking URL: {url}...")
                api_webcheck(url)
            else:
                print(f"Checking URL: {url}...")
                api_webcheck_list(arg_list[1:])
        else:
            # Print help message if the command is not recognized
            self.parser.print_help()

# API CALLS FUNCTIONS   ------------------------------------------------------------------

# API etk_finance

# Obtiene el precio mas reciente del symbol y exchange especificados
def api_etk_finance_get_stock_currentprice(symbol, exchange):
    params = {'symbol': symbol, 'exchange': exchange}
    api_endpoint = api_url + '/etk_finance/get_stock_currentprice'
    print ('api_client: symbol --> ', symbol)
    print ('api_client: exchange --> ', exchange)
    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            current_price = response.json()
            if current_price:
                print(f'Current price of {symbol} on {exchange}: {current_price}')
            else:
                print(f"No data found for {symbol} on {exchange}.")
        else:
            print(f"Error occurred while fetching data for {symbol}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")

# Obtiene una lista de precioes historicos para un symbol y un exchange, desde la fecha start_date, hasta end_date
def api_etk_finance_get_hist_prices(symbol, exchange, start_date, end_date):
    params = {'symbol': symbol, 'exchange': exchange, 'start_date': start_date, 'end_date': end_date}
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            df_prices = response.json()
            if df_prices:
                print(f'Stock {symbol} prices from {start_date} to {end_date}')
                print(df_prices)
            else:
                print(f"No data found for {symbol} on {exchange} between {start_date} and {end_date}.")
        else:
            print(f"Error occurred while fetching data for {symbol}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")

# Obtiene la lista de simbolos o tickers del exchange especificado
def  api_etk_finance_get_tickers(exchange):
    # Set the query parameters
    params = {
        'exchange': exchange,
    }

    # Make a GET request to the /etk_finance endpoint with the query parameters
    try:
    # Make a GET request to the /etk_finance endpoint with the query parameters
        response = requests.get(f'{api_url}/etk_finance', params=params)

        # response.raise_for_status()
        if response.status_code == 200:
            print(f'SYMBOL LIST FOR {exchange}')
            # Extract the response data in JSON format
            tickers = response.json()
            # Print the response data
            print(tickers)
        else:
            # Handle the error
            print(f'ETK_Client: Request failed with status code {response.status_code}')

    except requests.exceptions.HTTPError as http_err:
        print(f'ETK_Client:  HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'ETK_Client: Other error occurred: {err}')

# API api_webcheck

# Imprime OK si la pagina web tiene acceso sin problemas, de otra forma retorna el error del request
def api_webcheck(url):
    # Set the query parameters
    params = {
        'url': url
    }
    
    try:
        response = requests.get(api_url, params={'url': url})
        status_code = response.status_code
        if status_code == 200:
            print(f"ETK_Client: {url} is OK")
        elif status_code == 404:
            print(f"ETK_Client: {url} not found")
        else:
            print(f"ETK_Client: {url} returned status code {status_code}")
    except requests.exceptions.RequestException as e:
        print(f"ETK_Client: An error occurred while checking {url}: {e}")

# Imprime OK en cada elemento de la lista de urls proporcionada si tiene acceso sin problemas, 
# de otra forma retorna el error del request para cada item
def api_webcheck_list(url_list):
    # Set the query parameters
    params = {
        'urls': url_list
    }
        
    try:
        response = requests.post(api_url, json={'urls': url_list})
        results = response.json()
        for url, status_code in results.items():
            if status_code == 200:
                print(f"ETK_Client: {url} is OK")
            elif status_code == 404:
                print(f"ETK_Client: {url} not found")
            else:
                print(f"ETK_Client: {url} returned status code {status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking URLs: {e}")


# -------------------------
#   M A I N
# -------------------------
if __name__ == '__main__':
    clear_screen()
    args = sys.argv
    print(f">>> Command line arguments: {args}")
    if __name__ == "__main__":
        args = sys.argv[1:]  # Ignore the first element, which is the name of the Python script
    print(f">>> Command line arguments: {args}")
    
    client = APIClient()
    args = client.parser.parse_args()
    print('dispatcher')
    print(args)
    client.dispatcher(args)
    
    
# EXAMPLES OF USE ------------------------------------------------------------------------------------------------------
# Get the current stock price for AAPL on NASDAQ
# python api_client.py etk_finance get_stock_currentprice AAPL NASDAQ

# Get historical stock prices for AAPL on NASDAQ between 2020-01-01 and 2021-01-01 and save to a file called prices.csv
# python api_client.py etk_finance get_hist_prices AAPL NASDAQ -f prices.csv 2020-01-01 2021-01-01

# Get a list of tickers and save to a file called tickers.txt
# python api_client.py etk_finance get_ticker_list -f tickers.txt

# Check if google.com is up
# python api_client.py webcheck https://www.google.com


'''

def  api_etk_finance_get_tickers(exchange):
    myData = etk_finance('output_plus.xlsx', username='oariasz72', password='Megatrends1') 
    print(f'GET TICKERS LIST FOR THE EXCHANGE {exchange} ------------------')
    tickers = myData.get_tickers(exchange)
    if len(tickers) > 0:
        print(f'SYMBOL LIST FOR {exchange}')
        print(tickers)



'''