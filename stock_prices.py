import numpy as np
import pandas as pd
from datetime import datetime
from concurrent import futures
from pandas_datareader.data import DataReader
import argparse

# adding the option to select parameter for years
parser = argparse.ArgumentParser()
parser.add_argument("--years_back", default=8, type=int, help="How many years for analysis.")

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
    success_tickers, failed_tickers = [], []

    for ticker in tickers_list:
        success_flag = get_stock(ticker)
        if success_tickers:
            success_tickers.append(ticker)
        else:
            failed_tickers.append(ticker)

    return success_tickers, failed_tickers