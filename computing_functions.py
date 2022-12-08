from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import time
import statistics

def market_betas(excess_returns, market):
    starting_time = time.time()

    excess_returns_index = excess_returns.index.copy()
    excess_returns.reset_index(inplace=True)
    excess_returns.drop(['Date'], axis=1, inplace=True)

    betas = excess_returns.copy()
    betas.loc[:] = np.nan

    column = 0
    for stock in excess_returns.columns:
        for row in range(len(excess_returns[stock])-253):
            y = excess_returns.iloc[row:(row + 253), :]
            y = y.loc[:, stock].values.reshape(-1, 1)
            x = market.iloc[row:(row + 253), :]
            x = x.loc[:,'Mkt-RF'].values.reshape(-1, 1)

            model = LinearRegression(fit_intercept=False).fit(x, y)
            betas.iloc[row + 253,column] = model.coef_
        column += 1

        #setting index back to date
    excess_returns.set_index(excess_returns_index, inplace=True)
    betas.set_index(excess_returns_index, inplace=True)

    betas = betas.iloc[253:, :] # cutting off NAs

    elapsed_time = time.time() - starting_time
    print('Elapsed time:', round(elapsed_time,3) , 'seconds.')
    return betas

def size_betas(excess_returns, size):
    starting_time = time.time()

    excess_returns_index = excess_returns.index.copy()
    excess_returns.reset_index(inplace=True)
    excess_returns.drop(['Date'], axis=1, inplace=True)

    betas = excess_returns.copy()
    betas.loc[:] = np.nan

    column = 0
    for stock in excess_returns.columns:
        for row in range(len(excess_returns[stock])-253):
            # print(f'stock:{stock}, row: {row}')
            y = excess_returns.iloc[row:(row + 253), :]
            y = y.loc[:, stock].values.reshape(-1, 1)
            x = size.iloc[row:(row + 253), :]
            x = x.loc[:,stock].values.reshape(-1, 1)

            model = LinearRegression(fit_intercept=False).fit(x, y)
            betas.iloc[row + 253,column] = model.coef_
        column += 1

        #setting index back to date
    excess_returns.set_index(excess_returns_index, inplace=True)
    betas.set_index(excess_returns_index, inplace=True)

    betas = betas.iloc[253:, :] # cutting off NAs

    elapsed_time = time.time() - starting_time
    print('Elapsed time:', round(elapsed_time,3) , 'seconds.')
    return betas

def str_betas(excess_returns, str):
    starting_time = time.time()

    excess_returns_index = excess_returns.index.copy()
    excess_returns.reset_index(inplace=True)
    excess_returns.drop(['Date'], axis=1, inplace=True)

    betas = excess_returns.copy()
    betas.loc[:] = np.nan

    column = 0
    for stock in excess_returns.columns:
        for row in range(len(excess_returns[stock])-253):
            y = excess_returns.iloc[row:(row + 253), :]
            y = y.loc[:, stock].values.reshape(-1, 1)
            x = str.iloc[row:(row + 253), :]
            x = x.loc[:,'ST_Rev'].values.reshape(-1, 1)

            model = LinearRegression(fit_intercept=False).fit(x, y)
            betas.iloc[row + 253,column] = model.coef_
        column += 1

        #setting index back to date
    excess_returns.set_index(excess_returns_index, inplace=True)
    betas.set_index(excess_returns_index, inplace=True)

    betas = betas.iloc[253:, :] # cutting off NAs

    elapsed_time = time.time() - starting_time
    print('Elapsed time:', round(elapsed_time,3) , 'seconds.')
    return betas


def fama_macbeth(monthly_returns, monthly_mkt_betas, monthly_size_betas, monthly_str_betas):
    monthly_returns_index = monthly_returns.index.copy() # saving the index

    monthly_returns.reset_index(inplace=True)
    monthly_mkt_betas.reset_index(inplace=True)
    monthly_size_betas.reset_index(inplace=True)
    monthly_str_betas.reset_index(inplace=True)

    monthly_returns.drop(['Date'], axis=1, inplace=True)
    monthly_mkt_betas.drop(['Date'], axis=1, inplace=True)
    monthly_size_betas.drop(['Date'], axis=1, inplace=True)
    monthly_str_betas.drop(['Date'], axis=1, inplace=True)

    gammas = monthly_returns.copy()
    gammas.loc[:] = np.nan

    for row in range(len(monthly_returns.index)):
        y = monthly_returns.iloc[row, :].values.reshape(-1, 1)
        x = pd.concat([monthly_mkt_betas.iloc[0, :], monthly_size_betas.iloc[0, :], monthly_str_betas.iloc[0, :]], axis=1).values.reshape(-1, 3)
        
        model = LinearRegression(fit_intercept=True).fit(x, y)
        intercept = model.intercept_[0]
        mkt_gamma = model.coef_[0][0]
        size_gamma = model.coef_[0][1]
        str_gamma = model.coef_[0][2]
        gammas.iloc[row, 0] = intercept
        gammas.iloc[row, 1] = mkt_gamma
        gammas.iloc[row, 2] = size_gamma
        gammas.iloc[row, 3] = str_gamma
        
    gammas.set_index(monthly_returns_index, inplace=True)
    gammas = gammas.iloc[:, 0:4]
    gammas.columns = ['intercept', 'mkt', 'size', 'str']

    monthly_returns.set_index(monthly_returns_index, inplace=True)
    monthly_mkt_betas.set_index(monthly_returns_index, inplace=True)
    monthly_size_betas.set_index(monthly_returns_index, inplace=True)
    monthly_str_betas.set_index(monthly_returns_index, inplace=True)
    
    return gammas
    

def results_table(gammas):
    intercept_mean = statistics.mean(gammas['intercept'])
    intercept_sd = statistics.stdev(gammas['intercept'])
    intercept_tstat = intercept_mean/intercept_sd
    mkt_mean = statistics.mean(gammas['mkt'])
    mkt_sd = statistics.stdev(gammas['mkt'])
    mkt_tstat = mkt_mean/mkt_sd
    size_mean = statistics.mean(gammas['size'])
    size_sd = statistics.stdev(gammas['size'])
    size_tstat = size_mean/size_sd
    str_mean = statistics.mean(gammas['str'])
    str_sd = statistics.stdev(gammas['str'])
    str_tstat = str_mean/str_sd

    fama_macbeth = pd.DataFrame(index=range(3),columns=range(4))
    fama_macbeth.loc[0,0] = intercept_mean
    fama_macbeth.loc[1,0] = intercept_sd
    fama_macbeth.loc[2,0] = intercept_tstat
    fama_macbeth.loc[0,1] = mkt_mean
    fama_macbeth.loc[1,1] = mkt_sd
    fama_macbeth.loc[2,1] = mkt_tstat
    fama_macbeth.loc[0,2] = size_mean
    fama_macbeth.loc[1,2] = size_sd
    fama_macbeth.loc[2,2] = size_tstat
    fama_macbeth.loc[0,3] = str_mean
    fama_macbeth.loc[1,3] = str_sd
    fama_macbeth.loc[2,3] = str_tstat
    fama_macbeth.loc[0,4] = 'mean'
    fama_macbeth.loc[1,4] = 'st. dev'
    fama_macbeth.loc[2,4] = 't-stat'
    fama_macbeth.columns = ['intercept', 'mkt', 'size', 'str', 'statistics']
    fama_macbeth.set_index('statistics', inplace=True)
    
    return fama_macbeth