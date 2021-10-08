# PROFIT OF 55.6k

import yfinance as yf
import time
import talib
import pandas as pd
import datetime

col_list = ["Symbol"]
symbols = pd.read_csv("futureandoptionstocks.csv", usecols=col_list)
totalprofit = 0
meanprofit = 0
maxprofit = 0
meanloss = 0
maxloss = 0
profits = 0
losses = 0
numtrades = 0

start = datetime.time(10, 0, 0)
end = datetime.time(16, 0, 0)

for i in range(int(len(symbols)/2)):
    symbol = symbols["Symbol"][2*i]

    df = pd.read_csv(f'testdata1/{symbol}.csv')
    df1d = pd.read_csv(f'historicalData5thJune1D/{symbol}.csv')
    # df = yf.Ticker(f"{symbol}.NS").history(period="10d", interval="5m")
    # df1d = yf.Ticker(f"{symbol}.NS").history(period="max", interval="1d")

    df["Ma_15"] = talib.EMA(df["Close"], timeperiod=15)
    df["Ma_50"] = talib.EMA(df["Close"], timeperiod=50)
    df["Ma_20"] = talib.EMA(df["Close"], timeperiod=20)
    df["VMa_20"] = talib.EMA(df["Volume"], timeperiod=20)
    rsi = talib.RSI(df["Close"])

    sections = []
    for i in range(len(rsi)):
        section = None
        if rsi[i] < 30:
            section = 'oversold'
        elif rsi[i] > 70:
            section = 'overbought'
        sections.append(section)

    position = None
    lastprofit = 0
    profit = 0
    quantity = round(200000/df["Close"][25])
    for i in df.index[-50:]:
        m5candles = len(df.index)-i
        # print(round(df['Close'][i], 2))
        d1candles = round(m5candles/75)
        dateIndex = (-1*d1candles)-1
        arr1 = df1d["High"][-50:]
        high = max(arr1)
        # arrhigh = df["High"][-75:]
        # high1 = max(arrhigh.iloc[:-1])
        if df["Ma_15"][i] > df["Ma_50"][i] and position != "Buy" and round(df['Close'][i], 2) >= 1.003*round(high, 2) and round(df['Close'][i-1], 2) <= 1.003*round(high, 2) and start <= datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() <= end:
            position = "Buy"
            lastprofit = profit
            profit -= round(df['Close'][i], 2)*quantity
            numtrades += 1
            print(
                f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")
        if df["Ma_20"][i] < df["Ma_50"][i] and position == "Buy":
            position = "Sell"
            lastprofit = profit
            profit += round(df['Close'][i], 2)*quantity
            print(
                f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")
            numtrades += 1
        if datetime.datetime.strptime(df['Datetime'][i], "%Y-%m-%d %H:%M:%S+05:30").time() >= datetime.time(15, 15, 0) and position == "Buy":
            position = "Sell"
            lastprofit = profit
            profit += round(df['Close'][i], 2)*quantity
            print(
                f"{position} : at {round(df['Close'][i],2)} and Time {df['Datetime'][i]}. Profit till now: {profit}")
            numtrades += 1

    if(abs(profit) > 100000):
        print(f'FINAL PROFIT for {symbol} = {round(lastprofit, 2)}')
        totalprofit += lastprofit
        if(lastprofit > 0):
            profits += 1
            meanprofit += lastprofit
            if(lastprofit > maxprofit):
                maxprofit = lastprofit
        if(lastprofit < 0):
            losses += 1
            meanloss += lastprofit
            if(lastprofit < maxloss):
                maxloss = lastprofit

    if(abs(profit) < 100000):
        print(f'FINAL PROFIT for {symbol} = {round(profit, 2)}')
        totalprofit += profit
        if(profit > 0):
            profits += 1
            meanprofit += profit
            if(profit > maxprofit):
                maxprofit = profit
        if(profit < 0):
            losses += 1
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
print(f"Num of trades: {numtrades}")
