from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


def market_betas(excess_returns, market):
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
    return betas