import streamlit as st
import datetime
import pandas as pd

df = pd.read_csv('symb.csv')
list1 = df['Symbol'].tolist()

date = st.sidebar.date_input('start date', datetime.date(2011, 1, 1))
st.write(date)

st.selectbox('Symbols',list1)