import os
import csv
import yfinance as yf
import pandas
import time


def snapshot_500():
    with open('datasets/Book1.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[1]
            Name = line.split(",")[0]
            #data = yf.download(symbol, start="2021-10-01", end="2021-11-23")
            data = yf.download(symbol, period="9mo", threads=True)
            data.to_csv('datasets/daily/{}.csv'.format(Name))


def single_stock(Name, symbol):
        data = yf.download(symbol, period="9mo", threads=True)
        data.to_csv('datasets/single_stock_data/{}.csv'.format(Name))



# For running on console infinitely

# i = 1
# while True:

#     snapshot()
#     time.sleep(300)
#     print(f'Ran {i} time')
#     i = i+1
