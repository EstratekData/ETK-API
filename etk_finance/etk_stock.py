import pandas as pd
import datetime
import os
from tvDatafeed import TvDatafeed, Interval
import openpyxl
import requests
import numpy as np
import logging
from datetime import datetime




# Class Interfaces -----------------------------------------------------------------------------------------------------------------------
# Class: App
# Methods
#       __init__()          Constructor de la clase
#           self
#           file_name:      nombre del Excel que contendra los resultados de salida
#           base_dir:       directorio base (default: None)
#
#       get_env_var(
#           self, 
#           variable_name:  nombre de la variable que se quiere obtener del sistema operativo
#           RETORNA:        el valor de la variable como string
# 
#       get_stock_data:     Recorre la lista de tickers buscando la data para cada ticker
#           self
#           the_tickers_df: dataframe con la lista de tickers de los cuales extraer informacion
#           the_exchange:   abreviacion del Exchange del que se quiere los tickers
#           stopiter:       cantidad de iteraciones permitidas, luego de las cuales se para el proceso (default: 0 // sin limites)
# 
#       update_excel:       Actualiza el Excel con los resultados de la informacion extraida de TraidingView
#           self, 
#           data_frame:     dataframe con toda la informacion extraida de los tickers previamente y almacaenada en la clase


        



class etk_finance:

    def __init__(self, file_name, base_dir=None, username = '', password = ''):
        self.file_name = file_name
        self.base_dir = base_dir
        print(base_dir)
        self.logger = logging.getLogger(__name__)
        
        column_headers = [ 'datetime' , 'symbol',  'open', 'high', 'low', 'close', 'volume']
        self.username = username   # self.get_env_var('ETK_FINANCE_USER')
        self.password = password            # self.get_env_var('ETK_FINANCE_PASSWORD')
                    
        if base_dir:
            self.file_path = os.path.join(base_dir, file_name)
        else:
            self.file_path = file_name
            
        if not os.path.isfile(self.file_path):
            print('\n')
            print(f"ETK_FINANCE: El archivo {self.file_path} no existe en el directorio base.")
            print('\n')
            data = []
            df = pd.DataFrame(data, columns=column_headers)
            # Genera una tabla vacia en Excel con las columnas column_headers
            df.to_excel(self.file_path, index=False, sheet_name='DB', header=True, startrow=0)            
        # self.writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
        
        
    # Calculates the days between a start_date and an end_date, both of them in a string format 'YYYY-MM-AA'
    def days_between(self, start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        return delta.days

    # Obtiene el valor de una variable de ambiente (OS) especificada
    def get_env_var(variable_name):
        value = os.environ.get(variable_name)
        if not value:
            print(f"Environment variable '{variable_name}' is unset.")
        return value

    def get_tickers(self, the_exchange):
        # Set the URL for the NYSE and NASDAQ ticker lists
        # nyse_url = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
        # nasdaq_url = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
        the_url = ''
        
        if (the_exchange == 'NYSE'):
            the_url ='https://datahub.io/core/nyse-other-listings/r/nyse-listed.csv'
        elif (the_exchange == 'NASDAQ'):
            the_url = 'https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.csv'
        else: 
            the_url = 'https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.csv'
            
        
        # Split the ticker lists from the full CSV string into lines        
        the_tickers = requests.get(the_url).text
        the_tickers = the_tickers.split("\n")
        the_tickers = [t for t in the_tickers if t] # Remove empty lines
        
        # Extract the ticker and name from each line, and add the exchange
        the_tickers = [[t.split(",")[0], t.split(",")[1], the_exchange] for t in the_tickers[1:]] # Skip the first line (column headers)
        return the_tickers


    def get_stock_data(self, ticker, exchange, interval, n_bars):
        print()
        tv = TvDatafeed(self.username, self.password)
        print(f'get_stock_data({self.username} --- {self.password})...')
        
        # get the current price of the stock
        try:
            df = tv.get_hist(symbol=ticker, exchange=exchange, interval=interval, n_bars = n_bars, extended_session=False)
        except Exception as e:
            self.logger.error(e)
            return None
        return df

    # Retorna un dataframe con toda la infomraación del ticker y el exchange 
    # INFO: (symbol, open, close, high, low, volume)
    def get_current_stock_price(self, ticker, exchange):
        print(f'get_current_stock_price({self.username} --- {self.password})...')
        # get the current price of the stock
        try:
            df = self.get_stock_data(ticker, exchange=exchange, interval=Interval.in_daily, n_bars = 1)
        except Exception as e:
            self.logger.error(e)
            return None
        return df
    
    # Retorna un dataframe con toda la infomraación del ticker y el exchange entre dos fechas
    # INFO: (symbol, open, close, high, low, volume)
    # FORMATOS DE start_date y end_date: 'YYYY-MM-DD'
    def get_stock_data_daily_interval(self, ticker, exchange, start_date, end_date ):
        nbars = self.days_between(start_date, end_date)
        tv = TvDatafeed(self.username, self.password)
        print(f'get_stock_data({self.username} --- {self.password})...')
        # start_date = pd.Timestamp('2023-01-01')
        # end_date = pd.Timestamp('2023-04-19')
        
        # get the current price of the stock
        try:
            df = self.get_stock_data(ticker, exchange=exchange, interval=Interval.in_daily, n_bars = nbars)
        except Exception as e:
            self.logger.error(e)
            return None
        return df

    # Recorre la lista de tickers buscando la data para cada ticker y acumulándola en el dataframe a retornar
    def get_exchange_data(self, the_tickers_df, the_exchange, stopiter = 0):
        the_tickers_df.reset_index()
        myExchange = the_exchange
        numberBars = 3
        data_results_df = pd.DataFrame([], columns=[ 'datetime' , 'symbol',  'open', 'high', 'low', 'close', 'volume'])
        tv = TvDatafeed(self.username, self.password)
        
        for index, row in the_tickers_df.iterrows():
            myTicker = row['Ticker']
            myTickerName = row['Ticker Name']

            # Depura lineas que vengan defectuosas
            # if len(myTicker) == 0: continue
            if myTickerName[0] == '"': myTickerName = myTickerName[1:]
            if len(myTickerName) > 60: myTickerName = myTickerName[:70].strip()
            myTickerName = myTickerName.replace('\n','')
            myTickerName = myTickerName.replace('\r','')

            # TODO: print (index, ' ', myTicker.ljust(7), ' ', myTickerName.ljust(70), '  ',  myExchange.ljust(8))  
            df = tv.get_hist(
                myTicker,
                myExchange,
                interval=Interval.in_daily,
                n_bars=numberBars,
                extended_session=False,
            )


            if df is None:
                print(f'Error con ticker: {myTicker}')
            else:
                print(myTicker, ':  ', len(df), ' entradas')
                data_results_df = pd.concat([data_results_df, df], ignore_index=True, axis=0)
          
            if stopiter > 0 and index == stopiter : break      # Limite de iteraciones para hacer pruebas
            # end for
            
        print('\n\n')
        print('Resultados a STOCK DATA.XLSX ---------------------------')
        print(data_results_df)

        # TODO: Hacer que no se borre el Excel anterior (buscar en Internet o GPT3)
        the_tickers_df.to_excel("tickers.xlsx",
            sheet_name=the_exchange)
        data_results_df.to_excel("stock data.xlsx",
            sheet_name=myExchange)
        return index
    
    # Actualiza el excel con los títulos solicitados
    def update_excel(self, data_frame):
        print('Archivo file_path: ', self.file_path)
        current_df = pd.read_excel(self.file_path, usecols='A:G', engine='openpyxl', header=0)
        print('CURRENT DATAFRAME:')
        print(current_df)
        print('NEW DATAFRAME:')
        print(data_frame)

        updated_df = pd.concat([current_df, data_frame], axis=0, ignore_index=True)      # agregar al final .drop_duplicates()
        print('UPDATED DATAFRAME:')
        print(updated_df)
        updated_df.to_excel(self.file_path, index=False, sheet_name='DB', header=True, startrow=0)   # Antes: startrow=len(current_df)+1
        
# End of etk_finance class implementation        


# TO DO List
#  1. Implementar método update_xlsx de etk_finance
#  2. Implementar un métoto para imprimir en pantalla
#  3. Retornar la cantidad de requisiciones que se hicieron a TradingView
#  4. Manejo de errores
#  5. Implementar método que obtenga el valor de un solo título
#  6. Probar con títulos venezolanos
#  7. Hacer API con estos métodos
#  8. Poner a correr año por año y probar hasta lograr hacer un gran batch que se 
#     traiga toda vaina
#  9. last_date y first_date de cada stock
# 10. Validar que la cantidad de fechas a extraer no exceda cierta cantidad en una corrida (e.g. 500.000)
