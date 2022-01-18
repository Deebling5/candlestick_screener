import os, pandas
import pandas as pd
import streamlit as st
from streamapp import *
from data_long import *
from data_500 import *
from twitter import *
import datetime
import plotly.graph_objects as go

Consol = []
Break = []
colab = []
ma = []
tma =[]
nulldf =[]

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

def consolbreak():
    for filename in os.listdir('datasets'):
        df = pandas.read_csv('datasets/{}'.format(filename))
    
        if is_consolidating(df):
            consol1 = filename + " is consolidating"
            Consol.append(consol1)
        if is_breaking_out(df):
            break1 = filename + " is Breaking Out"
            Break.append(break1)



def vol_break():
    for filename in os.listdir('datasets'):
        df = pandas.read_csv('datasets/{}'.format(filename))
        
        recent_candlesticks = df[-30:-1]
        global Volume
        global last
        Volume = int(recent_candlesticks['Volume'].mean())
        last = df[-1:]['Volume'].values[0]
        if last>Volume:
            vol1 = filename + " is volume breaking Out"
            colab.append(vol1)

def moving_avg():
    for filename in os.listdir('datasets'):
        df = pandas.read_csv('datasets/{}'.format(filename))
        
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
        


def consolidated():
    consolbreak()
    Consolidated = pd.DataFrame(Consol, columns=['Consolidate'])
    st.dataframe(Consolidated)

def breakout():
    consolbreak()
    Breakout = pd.DataFrame(Break, columns=['Breakout'])
    st.dataframe(Breakout)

def vol_breakout():
    vol_break()
    Vol_Breakout = pd.DataFrame(colab, columns=['Volume Breakout'])
    st.dataframe(Vol_Breakout)

def hundredma():
    moving_avg()
    hundredma = pd.DataFrame(ma, columns=['Hundred_MA'])
    st.dataframe(hundredma)

def twohundredma():
    moving_avg()
    twohundredma = pd.DataFrame(tma, columns=['two_Hundred_MA'])
    st.dataframe(twohundredma)
   
## Watchlist ## 

def consolidated_w():
    consolbreak_w()
    Consolidated_w = pd.DataFrame(Consol_w, columns=['Consolidate'])
    st.dataframe(Consolidated_w)


def breakout_w():
    consolbreak_w()
    Breakout_w = pd.DataFrame(Break_w, columns=['Breakout'])
    st.dataframe(Breakout_w)

def vol_breakout_w():
    vol_break_w()
    Vol_Breakout_w = pd.DataFrame(colab_w, columns=['Volume Breakout'])
    st.dataframe(Vol_Breakout_w)

def hundredma_w():
    moving_avg_w()
    hundredma_w = pd.DataFrame(ma_w, columns=['Hundred_MA'])
    st.dataframe(hundredma_w)
    

def twohundredma_w():
    moving_avg_w()
    twohundredma_w = pd.DataFrame(tma_w, columns=['two_Hundred_MA'])
    st.dataframe(twohundredma_w)
    
def none():
    st.dataframe(nulldf)
    
analysis_dict = {
        "None": none,
        "Consolidating": consolidated,
        "Breaking Out": breakout,
        "Volume Breakout": vol_breakout,
        "Hundred MA": hundredma,
        "Two Hundred MA": twohundredma,

}

analysis_dict_w = {
        "None": none,
        "Consolidating": consolidated_w,
        "Breaking Out": breakout_w,
        "Volume Breakout": vol_breakout_w,
        "Hundred MA": hundredma_w,
        "Two Hundred MA": twohundredma_w,

}

with st.sidebar:
    
    selected_analysis = st.selectbox("Nifty 500 Analysis", list(analysis_dict.keys()))
    st.write("---")
    
    selected_analysis_w = st.selectbox("Watchlist Analysis", list(analysis_dict_w.keys()))
    st.write("---")

    # Create a button
    if(st.button("Watchlist Snapshot")):
        snapshot()
        
    if(st.button("Nifty 500 Snapshot")):
        snapshot_500()
    st.write("---")
    

    
st.header(selected_analysis)
analysis_dict[selected_analysis]()

st.header(selected_analysis_w)
analysis_dict_w[selected_analysis_w]()

st.header('Twitter Search')
date_since = st.date_input('Since', datetime.date(2021, 12, 20))
numTweets = st.slider('Number of Tweets', 1, 500, 100)
symbol = st.text_input('Enter Search Term')

if symbol:
    numRuns = 1
    df = scraptweets(symbol, date_since, numTweets, numRuns)
  
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Text, df.Username, df.Created, df.Retweeted, df.URL],
                   fill_color='lavender',
                   align='left',font_size=12))
    ])


    st.plotly_chart(fig,use_container_width=True)
