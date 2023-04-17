import etk_stock
import pandas as pd


# ----------------------------------------------------------------------------------------------------------
# MAIN PROGRAM PARA LIBRERIA etk_stock y clase etk_finance -------------------------------------------------   
# ----------------------------------------------------------------------------------------------------------
  
# TODO: Homologar etk_stock y etk_finance
  
nreqs_to_trading_view = 0
STOP_COUNT = 10
myData = etk_stock.etk_finance('output_plus.xlsx') 
lista = myData.get_last_stock_price('AAPL','NASDAQ')
print(lista)
print('Done!')
    
quit()   # Finaliza la ejecución

