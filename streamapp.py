import os, pandas
import pandas as pd
import streamlit as st

Consol_w = []
Break_w = []
colab_w = []
ma_w = []
tma_w = []


def is_consolidating(df, percentage=2.5):
    recent_candlesticks = df[-15:]
    #print(percentage)
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()

    threshold = 1 - (percentage   
                     / 100)
    if min_close > (max_close * threshold):
        return True        
    
    return False

def is_breaking_out(df, percentage=3):
    last_close = df[-1:]['Close'].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-16:-1]

        if last_close > recent_closes['Close'].max():
            return True

    return False


def consolbreak_w():
    for filename in os.listdir('datasets/long'):
        df = pandas.read_csv('datasets/long/{}'.format(filename))
    
        if is_consolidating(df):
            consol1 = filename + " is consolidating"
            Consol_w.append(consol1)
        if is_breaking_out(df):
            break1 = filename + " is Breaking Out"
            Break_w.append(break1)



def vol_break_w():
    global colab_w
    colab_w = []
    
    for filename in os.listdir('datasets/long'):
        df = pandas.read_csv('datasets/long/{}'.format(filename))
        recent_candlesticks = df[-30:-1]
        global Volume
        global last
        Volume = int(recent_candlesticks['Volume'].mean())
        last = df[-1:]['Volume'].values[0]
        if last>Volume:
            vol1 = filename + " is volume breaking Out"
            colab_w.append(vol1)

def moving_avg_w():
    global ma_w
    ma_w = []
    global tma_w
    tma_w =[]
    
    for filename in os.listdir('datasets/long'):
        
        df = pandas.read_csv('datasets/long/{}'.format(filename))
        df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
        df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
        last_close = df[-1:]['Adj Close'].values[0]
        hma = df[-1:]['100ma'].values[0]
        twoma = df[-1:]['200ma'].values[0]
        per = (1/100)*last_close
    
        if abs(last_close - hma) <= per:
            x = filename + " is around 100 MA"
            ma_w.append(x)
    
        if abs(last_close - twoma) <= per:
            y = filename + " is around 200 MA"
            tma_w.append(y)
        


    






