# PROFIT OF 58.8k

import yfinance as yf
import time
import numpy as np
import talib
import pandas as pd
import datetime
import csv

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, LSTM

params = {"smallema": 10,
          "bigema": 50,
          "smallemasell": 5,
          "bigemasell": 10,
          "starthour": 9,
          "endhour": 16,
          "alpha": 1.0}


col_list = ["Symbol"]
symbols = pd.read_csv("futureandoptionstocks.csv", usecols=col_list)

amountPerTrade = 200000


# meanprofit = 0
# maxprofit = 0
# meanloss = 0
# maxloss = 0
# profits = 0
# losses = 0


def evaluateProfit(params):
    totalprofit = 0
    if(params['starthour'] >= params['endhour']):
        print(f'Score: 0')
        return 0
    if(params['smallema'] >= 2*params['bigema']):
        print(f'Score: 0')
        return 0
    if(params['smallemasell'] >= 2*params['bigemasell']):
        print(f'Score: 0')
        return 0

    start = datetime.time(params['starthour'], 0, 0)
    end = datetime.time(params['endhour'], 0, 0)
    for i in range(int(len(symbols)/2)):
        symbol = symbols["Symbol"][2*i]

        df = pd.read_csv(f'testdata/{symbol}.csv')
        df1d = pd.read_csv(f'historicalData5thJune1D/{symbol}.csv')
        # df.to_csv(f'historicalData5thJune/{symbol}.csv')
        df["Ma_small"] = talib.EMA(
            df["Close"], timeperiod=5*params['smallema'])
        df["Ma_big"] = talib.EMA(df["Close"], timeperiod=10*params['bigema'])
        df["Ma_smallsell"] = talib.EMA(
            df["Close"], timeperiod=5*params['smallemasell'])
        df["Ma_bigsell"] = talib.EMA(
            df["Close"], timeperiod=10*params['bigemasell'])
        # rsi = talib.RSI(df["Close"])

        position = None
        lastprofit = 0
        profit = 0
        quantity = round(amountPerTrade/df["Ma_small"][200])
        for i in df.index[199:]:
            m5candles = len(df.index)-i
            d1candles = round(m5candles/75)
            dateIndex = (-1*d1candles)-1
            arr1 = df1d["High"][dateIndex-50:dateIndex]
            high = max(arr1.iloc[:-1])
            if df["Ma_small"][i] > df["Ma_big"][i] and position != "Buy" and round(df['Close'][i], 2) >= params['alpha']*round(high, 2) and round(df['Close'][i-1], 2) <= params['alpha']*round(high, 2) and start <= datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() <= end:
                position = "Buy"
                lastprofit = profit
                profit -= round(df['Close'][i], 2)*quantity
                # print(
                #     f"{position} : at {round(df['Close'][i],2)} and Time {i}. Profit till now: {profit}")
            if df["Ma_smallsell"][i] < df["Ma_bigsell"][i] and position == "Buy":
                position = "Sell"
                lastprofit = profit
                profit += round(df['Close'][i], 2)*quantity
                # print(
                #     f"{position} : at {round(df['Close'][i],2)} and Time {i}. Profit till now: {profit}")
            if datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() >= datetime.time(15, 15, 0) and position == "Buy":
                position = "Sell"
                lastprofit = profit
                profit += round(df['Close'][i], 2)*quantity

        if(abs(profit) > 100000):
            # print(f'FINAL PROFIT for {symbol} = {round(lastprofit, 2)}')
            totalprofit += lastprofit
            # if(lastprofit > 0):
            #     profits += 1
            #     meanprofit += lastprofit
            #     if(lastprofit > maxprofit):
            #         maxprofit = lastprofit
            # if(lastprofit < 0):
            #     losses += 1
            #     meanloss += lastprofit
            #     if(lastprofit < maxloss):
            #         maxloss = lastprofit

        if(abs(profit) < 100000):
            # print(f'FINAL PROFIT for {symbol} = {round(profit, 2)}')
            totalprofit += profit
            # if(profit > 0):
            #     profits += 1
            # meanprofit += profit
            # if(profit > maxprofit):
            #     maxprofit = profit
            # if(profit < 0):
            #     losses += 1
            # meanloss += profit
            # if(profit < maxloss):
            #     maxloss = profit

    print(f'Score: {round(totalprofit/100000, 2)}')
    return round(totalprofit/100000, 2)
    # meanloss /= losses
    # meanprofit /= profits
    # print(f"TOTAL PROFIT = {totalprofit}")
    # print(f"PROFITS = {profits}")
    # print(f"MEAN PROFIT = {meanprofit}")
    # print(f"MAX PROFIT = {maxprofit}")
    # print(f"LOSSES = {losses}")
    # print(f"MEAN LOSS = {meanloss}")
    # print(f"MAX LOSS = {maxloss}")
