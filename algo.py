# PROFIT OF 46.6k

import yfinance as yf
import time
import talib
import pandas as pd

col_list = ["Symbol"]
symbols = pd.read_csv("futureandoptionstocks.csv", usecols=col_list)
totalprofit = 0
for i in range(int(len(symbols)/2)):
    symbol = symbols["Symbol"][2*i]

    df = yf.Ticker(f"{symbol}.NS").history(period="2y", interval="1H")
    df.to_csv(f"historicalData3H/{symbol}.csv")

#     df["Ma_5"] = round(df["Close"].rolling(window=5).mean(), 2)
#     df["Ma_10"] = round(df["Close"].rolling(window=10).mean(), 2)
#     rsi = talib.RSI(df["Close"])

#     sections = []
#     for i in range(len(rsi)):
#         section = None
#         if rsi[i] < 30:
#             section = 'oversold'
#         elif rsi[i] > 70:
#             section = 'overbought'
#         sections.append(section)

#     position = None
#     lastprofit = 0
#     profit = 0
#     quantity = round(200000/df["Ma_5"][200])
#     for i in df.index[199:]:
#         arr1 = df["Close"][:i]
#         high = max(arr1)
#         if df["Ma_5"][i] > df["Ma_10"][i] and position != "Buy" and round(df['Close'][i], 2) >= round(high, 2):
#             position = "Buy"
#             lastprofit = profit
#             profit -= round(df['Close'][i], 2)*quantity
#             # print(
#             #     f"{position} : at {round(df['Close'][i],2)} and Time {i}. Profit till now: {profit}")
#         if df["Ma_5"][i] < df["Ma_10"][i] and position == "Buy" and rsi[i] > 30:
#             position = "Sell"
#             lastprofit = profit
#             profit += round(df['Close'][i], 2)*quantity
#             # print(
#             #     f"{position} : at {round(df['Close'][i],2)} and Time {i}. Profit till now: {profit}")

#     if(abs(profit) > 100000):
#         print(f'FINAL PROFIT for {symbol} = {round(lastprofit, 2)}')
#         totalprofit += lastprofit

#     if(abs(profit) < 50000):
#         print(f'FINAL PROFIT for {symbol} = {round(profit, 2)}')
#         totalprofit += profit
# print(totalprofit)
