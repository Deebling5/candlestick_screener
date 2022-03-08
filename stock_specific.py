from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()  

global df 

def stock_specific(symbol,per,inter):

    data = pdr.get_data_yahoo(symbol, period=per, interval=inter)
    df = data.reset_index(level='Date')
    has_value = ~df["High"].isna()
    
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
    df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
    df['21ma'] = df['Adj Close'].rolling(window=21, min_periods=0).mean()
    
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'],
                                         high=df['High'], low=df['Low'], close=df['Close'], name=symbol)])
    
    fig.add_trace(
        go.Scatter(mode='lines', x=df[has_value]['Date'], y=df[has_value]["200ma"], line={'color': 'green', 'width': 1}, name='200 MA'))
    
    fig.add_trace(
        go.Scatter(mode='lines', x=df[has_value]['Date'], y=df[has_value]["100ma"], line={'color': 'blue', 'width': 1}, name='100 MA'))
        
    fig.add_trace(
        go.Scatter(mode='lines', x=df[has_value]['Date'], y=df[has_value]["21ma"], line={'color': 'orange', 'width': 1}, name='21 MA'))
    
    #fig.add_trace(
    #    go.Scatter(mode="markers",
    #               x=df['Date'],
    #               y=df["High"]
    #               ))
    
    fig.update_layout(
        autosize=False,
        width=1000,
        height=800,)
    
    hunma = df['100ma'].iloc[-1]
    twoma = df['200ma'].iloc[-1]
    twentyma = df['21ma'].iloc[-1]
    cmp = df['Adj Close'].iloc[-1]
    if df['Adj Close'].iloc[-1] - df['Open'].iloc[-1] > 0:
        state = '+'
    else:
        state = '-'
        
    
    hunma = round(hunma,2)
    twoma = round(twoma, 2)
    twentyma = round(twentyma, 2)
    cmp = round(cmp, 2)
    
    return fig, hunma, twoma, twentyma, cmp, state

# DLF
# ICICI
# Federal
# LIChfin
# Tata mot
# Tata power
# Exide ind
# bandhan bank
#sbi

