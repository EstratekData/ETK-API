from etk_stock import etk_finance
import pandas as pd
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------------------------------------------------------------
# MAIN PROGRAM PARA LIBRERIA etk_stock y clase etk_finance -------------------------------------------------   
# ----------------------------------------------------------------------------------------------------------
  
# TODO: Homologar etk_stock y etk_finance
clear_screen()  
  
nreqs_to_trading_view = 0
STOP_COUNT = 10
myData = etk_finance('output_plus.xlsx', username='oariasz72', password='Megatrends1') 


my_stock = 'AAPL'
my_exchange = 'NASDAQ'

print(f'GET CURRENT STOCK PRICE {my_stock} / {my_exchange} ------------------')
df_prices = myData.get_current_stock_price(my_stock, my_exchange)
if df_prices is not None:
    print('Resultados')
    print(df_prices)
    
'''    
print('GET DAILY STOCK PRICE OF Apr-2023 {my_stock} / {my_exchange} ------------------')
df_prices = myData.get_stock_data_daily_interval(my_stock, my_exchange, '2023-04-01', '2023-04-19')
if df_prices is not None:
    print('Resultados Abril')
    print(df_prices)    
'''

print(f'FULL EXCHANGE STOCK DATA OF Apr-2023 {my_stock} / {my_exchange} ------------------')
# 1. Get the ticker lists from the URLs
nasdaq_tickers_list = myData.get_tickers('NYSE')
# print ('NYSE Tickers List')
# print(nyse_tickers_list)
nasdaq_tickers_df = pd.DataFrame(nasdaq_tickers_list, columns=['Ticker', 'Ticker Name', 'Exchange'])
nasdaq_tickers_df = pd.read_excel('tickers.xlsx')      # Extrae los tickers desde el archivo tickers.xlsx

print('nasdaq tickers')
print(nasdaq_tickers_df)
print('------------------------------------')
df_prices = myData.get_exchange_data(nasdaq_tickers_df, my_exchange, '2023-04-01', '2023-04-19', stopiter=10)
print(' ')

if df_prices is not None:
    print('Resultados Abril')
    print(df_prices)    
    myData.update_excel('output_plus.xlsx')
print(f'Saving results to {myData.file_path}...')
myData.update_excel(df_prices)
print (f'Registros agregados: {myData.iterador}')
print('THE END')
# print('The last price for {my_stock} at the exchange {my_exchange} is: ${my_price}')
quit() 




# index
# stock_data = tv.get_hist(symbol='F',exchange='NSE',interval=Interval.in_daily, n_bars=1000)

# futures continuous contract
# nifty_futures_data = tv.get_hist(symbol='NIFTY',exchange='NSE',interval=Interval.in_1_hour,n_bars=1000,fut_contract=1)

# crudeoil
# crudeoil_data = tv.get_hist(symbol='CRUDEOIL',exchange='MCX',interval=Interval.in_1_hour,n_bars=5000,fut_contract=1)

# downloading data for extended market hours
# extended_price_data = tv.get_hist(symbol="EICHERMOT",exchange="NSE",interval=Interval.in_1_hour,n_bars=500, extended_session=False)
