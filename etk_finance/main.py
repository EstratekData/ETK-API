from etk_stock import etk_finance
import pandas as pd


# ----------------------------------------------------------------------------------------------------------
# MAIN PROGRAM PARA LIBRERIA etk_stock y clase etk_finance -------------------------------------------------   
# ----------------------------------------------------------------------------------------------------------
  
# TODO: Homologar etk_stock y etk_finance
  
nreqs_to_trading_view = 0
STOP_COUNT = 10
myData = etk_finance('output_plus.xlsx', username='oariasz72', password='Megatrends1') 


my_stock = 'AAPL'
my_exchange = 'NASDAQ'

print('GET CURRENT STOCK PRICE {my_stock} / {my_exchange}')
df_prices = myData.get_current_stock_price(my_stock, my_exchange)
if df_prices is not None:
    print('Resultados')
    print(df_prices)
    
print('GET DAILY STOCK PRICE OF Apr-2023 {my_stock} / {my_exchange}')
df_prices = myData.get_stock_data_daily_interval(my_stock, my_exchange, '2023-04-01', '2023-04-19')
if df_prices is not None:
    print('Resultados Abril')
    print(df_prices)    
    
print('THE END')
# print('The last price for {my_stock} at the exchange {my_exchange} is: ${my_price}')
quit() 



# 1. Get the ticker lists from the URLs
nyse_tickers_list = myData.get_tickers('NYSE')
print ('NYSE Tickers List')
print(nyse_tickers_list)
nyse_tickers_df = pd.DataFrame(nyse_tickers_list, columns=['Ticker', 'Ticker Name', 'Exchange'])

nasdaq_tickers_list = myData.get_tickers('NASDAQ')
print ('NASDAQ Tickers List')
print(nasdaq_tickers_list)
nasdaq_tickers_df = pd.DataFrame(nasdaq_tickers_list, columns=['Ticker', 'Ticker Name', 'Exchange'])

# Aquí se consolidan todos los tickers con sus exchanges. 
# NO SABEMOS SI ES NECESARIO HACER ESTO AUN
# TODO: Chequear código
total_tickers_df = pd.DataFrame([], columns=['Ticker', 'Ticker Name', 'Exchange'])
total_tickers_df = pd.concat([total_tickers_df, nyse_tickers_df])
total_tickers_df = pd.concat([total_tickers_df, nasdaq_tickers_df])

# 2. Extractor para todos los ticker posibles

# TODO: myData.get_stock_data(nyse_tickers_df,'NYSE', STOP_COUNT)
nreqs_to_trading_view += myData.get_stock_data(nyse_tickers_df,'NYSE', STOP_COUNT)  
print('\n Total Requests a TradingView: ', nreqs_to_trading_view)

print('\n\nSaving Excel file...')

myData.update_excel(nyse_tickers_df)
myData.update_excel(nasdaq_tickers_df)
print('Done!')
    
quit()   # Finaliza la ejecución




print('\nNYSE Tickers ----------------------')
a = np.array(nyse_tickers)
a = a[:,0]
i = 1
print (*a,   sep = "\n")

c = input()

# print('\nNASDAQ Tickers ----------------------')
# print (nyse_tickers)


c = input()


# total_stock = pd.DataFrame()



# EJEMPLOS

myTicker = 'AAPL'
myExchange = 'NASDAQ'   
# 'NYSE'
numberBars = 360

print('STOCK ----------------')
print('Ticker  : ', myTicker)
print('Exchange: ', myExchange)
print('Bars    : ', numberBars)
print('\n')

print('Obteniendo data de TradingView...')
stock_data_df = tv.get_hist(
    myTicker,
    myExchange,
    interval=Interval.in_daily,
    n_bars=numberBars,
    extended_session=False,
)

# Guarda el histórico en un Excel
print('Guardando en Excel...')
stock_data_df.to_excel("output.xlsx",
            sheet_name=myTicker)


print('Archivo Excel generado!')

print('STOCK HISTORICO ---------------')
print(stock_data_df)

# index
# stock_data = tv.get_hist(symbol='F',exchange='NSE',interval=Interval.in_daily, n_bars=1000)

# futures continuous contract
# nifty_futures_data = tv.get_hist(symbol='NIFTY',exchange='NSE',interval=Interval.in_1_hour,n_bars=1000,fut_contract=1)

# crudeoil
# crudeoil_data = tv.get_hist(symbol='CRUDEOIL',exchange='MCX',interval=Interval.in_1_hour,n_bars=5000,fut_contract=1)

# downloading data for extended market hours
# extended_price_data = tv.get_hist(symbol="EICHERMOT",exchange="NSE",interval=Interval.in_1_hour,n_bars=500, extended_session=False)
