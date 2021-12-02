import os, pandas
import pandas as pd
import streamlit as st

Consol = []
Break = []
colab = []
ma = []
tma =[]


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

for filename in os.listdir('datasets/long'):
    df = pandas.read_csv('datasets/long/{}'.format(filename))

    if is_consolidating(df):
        consol1 = filename + " is consolidating"
        Consol.append(consol1)
    if is_breaking_out(df):
        break1 = filename + " is Breaking Out"
        Break.append(break1)



def vol_break(df):
    recent_candlesticks = df[-30:-1]
    global Volume
    global last
    Volume = int(recent_candlesticks['Volume'].mean())
    last = df[-1:]['Volume'].values[0]
    if last>Volume:
        vol1 = filename + " is volume breaking Out"
        colab.append(vol1)

def moving_avg(df):
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
    df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
    last_close = df[-1:]['Adj Close'].values[0]
    hma = df[-1:]['100ma'].values[0]
    twoma = df[-1:]['200ma'].values[0]
    per = (1/100)*last_close

    if abs(last_close - hma) <= per:
        x = filename + " is around 100 MA"
        ma.append(x)

    if abs(last_close - twoma) <= per:
        y = filename + " is around 200 MA"
        tma.append(y)
        

for filename in os.listdir('datasets/long'):
    df = pandas.read_csv('datasets/long/{}'.format(filename))
    vol_break(df)
    moving_avg(df)
    

Consolidated = pd.DataFrame(Consol, columns=['Consolidate'])
Breakout = pd.DataFrame(Break, columns=['Breakout'])
Vol_Breakout = pd.DataFrame(colab, columns=['Volume Breakout'])
hundredma = pd.DataFrame(ma, columns=['Hundred_MA'])
twohundredma = pd.DataFrame(tma, columns=['two_Hundred_MA'])

st.dataframe(Consolidated)
st.dataframe(Breakout)
st.dataframe(Vol_Breakout)
st.dataframe(hundredma)
st.dataframe(twohundredma)





