# PROFIT OF 58.8k

from math import sqrt
from sklearn.utils.multiclass import type_of_target
import yfinance as yf
import time
import numpy as np
import talib
import pandas as pd
import datetime
import csv
import statistics
from colorama import Fore, Back, Style

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, LSTM


col_list = ["Symbol"]
symbols = pd.read_csv("futureandoptionstocks.csv", usecols=col_list)

amountPerTrade = 200000


meanprofit = 0
maxprofit = 0
meanloss = 0
maxloss = 0
profits = 0
losses = 0
numtrades = 0

totalprofit = 0
alpha = 0.00141
beta = 0.0049

for i in range(int(len(symbols)/2)):  # CYCLE THROUGH ALL STOCKS
    symbol = symbols["Symbol"][2*i]  # ANALYSE LOSSES

    df = pd.read_csv(f'testdata1/{symbol}.csv')
    #df1d = pd.read_csv(f'historicalData8thJune1D/{symbol}.csv')
    # df.to_csv(f'historicalData5thJune/{symbol}.csv')
    position = None
    target = 100000
    stoploss = 0
    lastprofit = 0
    profit = 0
    quantity = round(amountPerTrade/df["Close"][70])
    df["Ma_15"] = talib.EMA(
        df["Close"], timeperiod=15)
    df["Ma_50"] = talib.EMA(df["Close"], timeperiod=50)

    for i in df.index[75:]:
        # m5candles = len(df.index)-i
        # d1candles = round(m5candles/75)
        # dateIndex = (-1*d1candles)
        arr1 = df["High"][i-70:i]

        if df["Ma_15"][i] < df["Ma_50"][i] and position == "Buy":
            position = "Sell"
            lastprofit = profit
            numtrades += 1
            profit += round(df['Close'][i], 2)*quantity
            print(
                f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")

        if df["Close"][i] < stoploss and position == "Buy":
            position = "Sell"
            stoploss = 0
            numtrades += 1
            target = 100000
            lastprofit = profit
            profit += round(df['Close'][i], 2)*quantity
            print(
                f"SL HIT: {position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")

        if df["Close"][i] > target and position == "Buy":
            stoploss = target-(0.002*df['Close'][i])
            target = target+(0.005*df['Close'][i])

        if datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() >= datetime.time(15, 15, 0) and position == "Buy":
            position = "Sell"
            lastprofit = profit
            profit += round(df['Close'][i], 2)*quantity
            print(
                f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")
        openandcloses = np.append(df["Open"][i -
                                             4:i-1], df["Close"][i - 4:i-1])
        # print(len(highandlows))
        if((statistics.stdev(openandcloses) /
                df["Close"][df.index[i]]) > alpha):
            continue
        prime = np.append(openandcloses, (round(df['Close'][i], 2)))
        # print(df1d["Close"][dateIndex -
        #                     10:dateIndex])
        # print(prime)
        stdprime = statistics.stdev(
            prime)
        # prev = np.append(df1d["Close"][dateIndex -
        #                                10:dateIndex], (round(df['Close'][i-1], 2)))
        # stdprev = statistics.stdev(
        #     prev)
        # print(statistics.stdev(df1d["Close"][dateIndex-10:dateIndex]) /
        #       df1d["Close"][df1d.index[dateIndex]])
        # print(stdprime/df1d['Close'][df1d.index[dateIndex]])
        # print(stdprev/df1d['Close'][df1d.index[dateIndex]])
        # print(statistics.stdev(
        #     df1d["Close"][dateIndex-10:dateIndex])/df1d['Close'][df1d.index[dateIndex]])
        # print(stdprime/df1d['Close'][df1d.index[dateIndex]])
        # print(stdprev/df1d['Close'][df1d.index[dateIndex]])
        high = max(arr1.iloc[:-1])
        if position != "Buy" and df["Ma_15"][i] > df["Ma_50"][i] and stdprime/df["Close"][df.index[i]] >= beta and round(df['Close'][i], 2) > high and round(df['Close'][i], 2) > round(df['Close'][i-1], 2) and datetime.time(10, 0, 0) <= datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() <= datetime.time(13, 30, 0):
            position = "Buy"
            stoploss = max(0.99*df['Close'][i], 0.998*df['Close'][i-1])
            target = 1.01*df['Close'][i]
            numtrades += 1
            lastprofit = profit
            profit -= round(0.5*(df['Close'][i]+df['Close'][i-1]), 2)*quantity
            print(
                f"{position} {symbol} : at {round(0.5*(df['Close'][i]+df['Close'][i-1]))} and Time {df['Datetime'][i]}. Profit till now: {profit}")

    if(abs(profit) > 100000 and lastprofit != 0):

        totalprofit += lastprofit
        if(lastprofit > 0):
            profits += 1
            meanprofit += lastprofit
            print(Fore.GREEN +
                  f'FINAL PROFIT for {symbol} = {round(lastprofit, 2)}')
            if(lastprofit > maxprofit):
                maxprofit = lastprofit
        if(lastprofit < 0):
            losses += 1
            meanloss += lastprofit
            print(Fore.RED +
                  f'FINAL PROFIT for {symbol} = {round(lastprofit, 2)}')
            if(lastprofit < maxloss):
                maxloss = lastprofit

    if(abs(profit) < 100000 and profit != 0):

        totalprofit += profit
        if(profit > 0):
            profits += 1
            meanprofit += profit
            print(Fore.GREEN +
                  f'FINAL PROFIT for {symbol} = {round(profit, 2)}')
        if(profit > maxprofit):
            maxprofit = profit
        if(profit < 0):
            losses += 1
            print(Fore.RED +
                  f'FINAL PROFIT for {symbol} = {round(profit, 2)}')
            meanloss += profit
        if(profit < maxloss):
            maxloss = profit

meanloss /= losses
meanprofit /= profits
print(f"TOTAL PROFIT = {totalprofit}")
print(f"PROFITS = {profits}")
print(f"MEAN PROFIT = {meanprofit}")
print(f"MAX PROFIT = {maxprofit}")
print(f"LOSSES = {losses}")
print(f"MEAN LOSS = {meanloss}")
print(f"MAX LOSS = {maxloss}")
print(f"NUM TRADES = {numtrades}")
