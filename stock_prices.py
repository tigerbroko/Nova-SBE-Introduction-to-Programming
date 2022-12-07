import pandas as pd
from datetime import datetime
from pandas_datareader.data import DataReader
import time
# import numpy as np
# from concurrent import futures

def get_stock(ticker, years_back=5):
    today = datetime.now()
    start = datetime((today.year-years_back), today.month, today.day)
    end = today # could be changed if other range is desired
   
    # since some stocks might not be available, we use try/except
    try:
        stock_df = DataReader(ticker, 'yahoo', start, end)
        stock_df['Name'] = ticker

        csv_name = ticker + '.csv'
        stock_df.to_csv(csv_name)

        success_flag = True 
        print(f'{ticker} - SUCCESS')

    except:
        success_flag = False
        print(f'{ticker} - STOCK NOT FOUND')

    return success_flag

def get_stocks(tickers_list):
    starting_time = time.time()
    success_tickers, failed_tickers = [], []

    for ticker in tickers_list:
        success_flag = get_stock(ticker)
        if success_flag:
            success_tickers.append(ticker)
        else:
            failed_tickers.append(ticker)
    elapsed_time = time.time() - starting_time
    print('Elapsed time:', round(elapsed_time,3) , 'seconds.')
    return success_tickers, failed_tickers

def load_stocks(tickers_list):
    stocks_df_list = []
    for ticker in tickers_list:
        csv_name = ticker + '.csv'
        df = pd.read_csv(csv_name)
        stocks_df_list.append(df)
    
    return stocks_df_list

def get_close_prices(stocks_df_list, success_tickers):
    df_close_prices = stocks_df_list[0][['Date','Adj Close']]
 
    for index in range(1, len(stocks_df_list)):
        dataframe = stocks_df_list[index][['Date','Adj Close']]
        df_close_prices = df_close_prices.merge(dataframe, on='Date', how = 'inner')

    cp_columns_names = ['Date']
    cp_columns_names.extend(success_tickers)
    df_close_prices.columns = cp_columns_names
    df_close_prices.set_index('Date', inplace=True)

    return df_close_prices