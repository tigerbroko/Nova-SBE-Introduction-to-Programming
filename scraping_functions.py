import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
#import yfinance

def load_tickers(location):
    tickers = pd.read_csv(location, sep = ",")
    tickers = pd.DataFrame(tickers)
    tickers.columns = ["Index", "Ticker"]
    tickers = tickers['Ticker']

    return tickers

def mkt_cap_scraper(ticker):
    url = 'https://www.macrotrends.net/assets/php/market_cap.php?t=' + ticker
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    string = str(soup)

    # in this section, we get rid of the unwanted characters in the string
    stripped_begin = string.split('var chartData = [{', 1)[1]
    stripped_end = stripped_begin.split('];\r\n\r', 1)[0]
    stripped_end = re.sub('"date":"','',stripped_end)
    stripped_end = re.sub('},{',';',stripped_end)
    stripped_end = re.sub('","v1"','',stripped_end)
    stripped_end = re.sub('}','',stripped_end)

    stripped = stripped_end.split(';')

    # here we extract the date- and marketcap- parts of string,
    # convert them into desirable type, and save them into a Pandas dataframe

    date, mkt_cap = [], []

    for row in range(len(stripped)):
        datum = stripped[row][:10]
        datum = datetime.strptime(datum, '%Y-%m-%d')
        mc = stripped[row][11:]

        date.append(datum)
        mkt_cap.append(float(mc))

    mkt_cap_tuples = list(zip(date,mkt_cap))
    df_mkt_cap = pd.DataFrame(mkt_cap_tuples, columns=['Date','Mkt_Cap'])

    return df_mkt_cap


