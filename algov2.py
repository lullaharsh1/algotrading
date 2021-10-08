# PROFIT OF 58.8k

from math import sqrt
import yfinance as yf
import time
import numpy as np
import talib
import pandas as pd
import datetime
import csv
import statistics

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, LSTM

params = {"candlecount": 4,
          "alpha": 0.00141,
          "beta": 0.0049}
paramsmodify = {"openhour": 10, "openminute": 15,
                "closehour": 15, "closeminute": 15}


col_list = ["Symbol"]
symbols = pd.read_csv("futureandoptionstocks.csv", usecols=col_list)

amountPerTrade = 200000


# meanprofit = 0
# maxprofit = 0
# meanloss = 0
# maxloss = 0
# profits = 0
# losses = 0


def evaluateProfit(paramsmodify):
    totalprofit = 0
    grandtotalprofit = 0
    numtrades = 0
    # if(params['starthour'] >= params['endhour']):
    #     print(f'Score: 0')
    #     return 0
    if(params['alpha'] >= params['beta']):
        print(f'Score: 0')
        return 0

    start = datetime.time(
        paramsmodify["openhour"], 15 * paramsmodify["openminute"], 0)
    end = datetime.time(paramsmodify["closehour"],
                        15*paramsmodify["closeminute"], 0)
    if(start > end):
        print(f'Score: 0')
        return 0
    # start = datetime.time(params['starthour'], 0, 0)
    # end = datetime.time(params['endhour'], 0, 0)
    for j in range(4):

        for i in range(int(len(symbols)/2)):  # CYCLE THROUGH ALL STOCKS
            symbol = symbols["Symbol"][2*i]

            df = pd.read_csv(f'testdata/{symbol}.csv')
            # df1d = pd.read_csv(f'historicalData5thJune1D/{symbol}.csv')
            # df.to_csv(f'historicalData5thJune/{symbol}.csv')
            target = 100000
            stoploss = 0
            position = None
            lastprofit = 0
            profit = 0
            quantity = round(amountPerTrade/df["Close"][200])
            df["Ma_15"] = talib.EMA(
                df["Close"], timeperiod=15)
            df["Ma_50"] = talib.EMA(df["Close"], timeperiod=50)

            for i in df.index[-(375*(j+1)):-(375*(j))]:
                # m5candles = len(df.index)-i
                # d1candles = round(m5candles/75)
                # dateIndex = (-1*d1candles)
                arr1 = df["Close"][i-70:i]
                high = max(arr1.iloc[:-1])

                if df["Ma_15"][i] < df["Ma_50"][i] and position == "Buy":
                    position = "Sell"
                    lastprofit = profit
                    profit += round(df['Close'][i], 2)*quantity
                    numtrades += 1
                    # print(
                    #     f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")

                if df["Close"][i] < stoploss and position == "Buy":
                    position = "Sell"
                    stoploss = 0
                    target = 100000
                    numtrades += 1
                    lastprofit = profit
                    profit += round(df['Close'][i], 2)*quantity
                    # print(
                    #     f"SL HIT: {position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")

                if df["Close"][i] > target and position == "Buy":
                    stoploss = target-(0.002*df['Close'][i])
                    target = target+(0.005*df['Close'][i])

                if datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() >= datetime.time(15, 15, 0) and position == "Buy":
                    position = "Sell"
                    lastprofit = profit
                    profit += round(df['Close'][i], 2)*quantity
                    # print(
                    #     f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")
                openandcloses = np.append(df["Open"][i -
                                                     params['candlecount']:i], df["Low"][i - params['candlecount']:i])
                std = statistics.stdev(
                    openandcloses) / df["Close"][df.index[i]]
                if(std > params['alpha']):
                    continue
                prime = np.append(openandcloses, (round(df['Close'][i], 2)))
                stdprime = statistics.stdev(
                    prime) / df["Close"][df.index[i]]

                # prev = np.append(highandlows, (round(df['Close'][i-1], 2)))
                # stdprev = statistics.stdev(
                #     prev) / df1d["Close"][df1d.index[dateIndex]]
                if position != "Buy" and df["Ma_15"][i] > df["Ma_50"][i] and round(df['Close'][i], 2) > high and stdprime >= params['beta'] and round(df['Close'][i], 2) > high and round(df['Close'][i], 2) > round(df['Close'][i-1], 2) and start <= datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() <= end:
                    position = "Buy"
                    lastprofit = profit
                    stoploss = max(0.99*df['Close'][i], 0.998*df['Close'][i-1])
                    target = 1.01*df['Close'][i]
                    profit -= round(df['Close'][i], 2)*quantity
                    numtrades += 1
                    # print(
                    #     f"{position} : at {round(df['Close'][i],2)} and Time {i}. Profit till now: {profit}")

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
            if(totalprofit < 0):
                totalprofit *= 4
            grandtotalprofit += totalprofit
            totalprofit = 0

    print(
        f'Score: {round(grandtotalprofit/(100000), 2)} for params: params = {paramsmodify} ')
    return round(totalprofit/(100000), 2)
    # meanloss /= losses
    # meanprofit /= profits
    # print(f"TOTAL PROFIT = {totalprofit}")
    # print(f"PROFITS = {profits}")
    # print(f"MEAN PROFIT = {meanprofit}")
    # print(f"MAX PROFIT = {maxprofit}")
    # print(f"LOSSES = {losses}")
    # print(f"MEAN LOSS = {meanloss}")
    # print(f"MAX LOSS = {maxloss}")
