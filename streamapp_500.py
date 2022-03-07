import os
import pandas as pd
import streamlit as st
from nifty_algo import *
from nifty_algo_500 import *
from data_long import *
from data_500 import *
from twitter import *
import datetime
import plotly.graph_objects as go



st.set_page_config(
    page_title="Stock Explorer - Abhijay",
    page_icon="🧊",
    initial_sidebar_state="auto",
    #menu_items={
    #    'Get Help': 'https://www.extremelycoolapp.com/help',
    #    'Report a bug': "https://www.extremelycoolapp.com/bug",
    #    'About': "This is an *extremely* cool app!"
    #}
)

page = st.sidebar.selectbox("Choose a page", ["Nifty 500 Explorer", "Twitter Search", 'Testing'])

def consolidated():
    consolbreak()
    Consolidated = pd.DataFrame(Consol, columns=['Consolidate'])
    st.table(Consolidated)


def breakout():
    consolbreak()
    Breakout = pd.DataFrame(Break, columns=['Breakout'])
    st.table(Breakout)


def vol_breakout():
    vol_break()
    Vol_Breakout = pd.DataFrame(colab, columns=['Volume Breakout'])
    st.table(Vol_Breakout)


def hundredma():
    moving_avg()
    hundredma = pd.DataFrame(ma, columns=['Hundred_MA'])
    st.table(hundredma)


def twohundredma():
    moving_avg()
    twohundredma = pd.DataFrame(tma, columns=['two_Hundred_MA'])
    st.table(twohundredma)

## Watchlist ##


def consolidated_w():
    consolbreak_w()
    Consolidated_w = pd.DataFrame(Consol_w, columns=['Consolidate'])
    st.table(Consolidated_w)


def breakout_w():
    consolbreak_w()
    Breakout_w = pd.DataFrame(Break_w, columns=['Breakout'])
    st.table(Breakout_w)


def vol_breakout_w():
    vol_break_w()
    Vol_Breakout_w = pd.DataFrame(colab_w, columns=['Volume Breakout'])
    st.dataframe(Vol_Breakout_w)


def hundredma_w():
    moving_avg_w()
    hundredma_w = pd.DataFrame(ma_w, columns=['Hundred_MA'])
    st.table(hundredma_w)


def twohundredma_w():
    moving_avg_w()
    twohundredma_w = pd.DataFrame(tma_w, columns=['two_Hundred_MA'])
    st.table(twohundredma_w)


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

if page == "Nifty 500 Explorer":
    
    st.title('Nifty 500 Explorer')
    st.write("---")
    
    if(st.button("Pull Data")):
        snapshot_500()
    st.write("---")
        
    selected_analysis = st.selectbox(
        "Select Analysis", list(analysis_dict.keys()))
    st.write("---")

    #selected_analysis_w = st.selectbox(
    #    "Watchlist Analysis", list(analysis_dict_w.keys()))
    #st.write("---")

    ## Create a button
    #if(st.button("Watchlist Snapshot")):
    #    snapshot()

   
    st.subheader(selected_analysis)
    analysis_dict[selected_analysis]()

elif page == "Twitter Search":
    
    
    #st.header(selected_analysis_w)
    #analysis_dict_w[selected_analysis_w]()
    
    st.title('Twitter Search')
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
                       align='left', font_size=12))
        ])
    
        st.plotly_chart(fig, use_container_width=True)

else:
    st.title('Test app')
