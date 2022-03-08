
import os
import pandas as pd




nulldf = []


def is_consolidating(df, percentage=2.5):
    recent_candlesticks = df[-15:]
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


def consolbreak():
    Consol = []
    Break = []
    for filename in os.listdir('datasets/daily'):
        df = pd.read_csv('datasets/daily/{}'.format(filename))
    
        if is_consolidating(df):
            consol1 = filename + " is consolidating"
            Consol.append(consol1)
        if is_breaking_out(df):
            break1 = filename + " is Breaking Out"
            Break.append(break1)
    return Consol, Break

def vol_break():
    colab = []
    for filename in os.listdir('datasets/daily'):
        df = pd.read_csv('datasets/daily/{}'.format(filename))

        recent_candlesticks = df[-15:-1]
        global Volume
        global last
        Volume = int(recent_candlesticks['Volume'].mean())
        last = df[-1:]['Volume'].values[0]
        if last > Volume:
            vol1 = filename + " is volume breaking Out"
            colab.append(vol1)
    return colab

def moving_avg():
    ma = []
    tma = []
    for filename in os.listdir('datasets/daily'):
        df = pd.read_csv('datasets/daily/{}'.format(filename))

        df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
        df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
        last_close = df[-1:]['Adj Close'].values[0]
        hma = df[-1:]['100ma'].values[0]
        twoma = df[-1:]['200ma'].values[0]
        per = (1.5/100)*last_close

        if abs(last_close - hma) <= per:
            x = filename + " is around 100 MA"
            ma.append(x)

        if abs(last_close - twoma) <= per:
            y = filename + " is around 200 MA"
            tma.append(y)
    return ma, tma
