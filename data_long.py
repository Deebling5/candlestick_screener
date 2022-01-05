import os, csv
import yfinance as yf
import pandas
import time

def snapshot():
    with open('datasets/long.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[1]
            Name = line.split(",")[0]
            #data = yf.download(symbol, start="2021-10-01", end="2021-11-23")
            data = yf.download(symbol, period="6mo", threads = True)
            data.to_csv('datasets/long/{}.csv'.format(Name))
    return {
        "code": "success"
    }
# i = 1
# while True:
    
#     snapshot()
#     time.sleep(300)
#     print(f'Ran {i} time')
#     i = i+1