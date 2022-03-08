
# Candlestick Screener
Candlestick Screener has 3 functionalities :

1. Stock Search - Get candle screener chart with 100ma, 200ma, 21ma of your selected stock from list of ~1800 stocks on NSE

<img src="2nd_snip.png?raw=true" align="center" width="800" alt="after hours trades plot">

1.1. Expand Show Chart and this candle stick chart will open.

<img src="cs.png?raw=true" align="center" width="800" alt="after hours trades plot">

2. Nifty 500 Explorer - This data analysis tool can present you with Breaking out, Consolidating, Volume breakouts, stocks near moving averages in realtime.

<img src="snip.png?raw=true" align="center" width="800" alt="after hours trades plot">

3. Twitter Search - Search with keyword with date and number of tweets and you will get all related tweets (I use it to get latest tweets on my favourite stocks)

<img src="twitter.png?raw=true" align="center" width="800" alt="after hours trades plot">

## Setup
```shell
$ pip3 install -r requirements.txt
```
## How to Run quickly?

1. Clone the Repo
2. install Requirements
3. Run below command in CMD or other console.
```shell
streamlit run streamapp_500.py
```
4. A browser window will pop will Candle Screener open on localhost.
5. Pull latest data from button on top and Run your favourite analysis from list
6. Or Select your favourite stock and get everything on it.

## Technicalities
This section will show some of the functionality of each class; however, it is by no means exhaustive.

### Getting data
```python
# This function will fetch ticker data from yfinance (tickers present in csv file)
# Tickers such as - Tata Chemicals,TATACHEM.NS ; Tata Coffee,TATACOFFEE.NS

def snapshot():
    with open('datasets/long.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[1]
            Name = line.split(",")[0]
            data = yf.download(symbol, period="9mo", threads = True) 
            data.to_csv('datasets/long/{}.csv'.format(Name))
    return {
        "code": "success"
    }

# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# Valid periods : 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

# Its set to 9 months by default for calculating 200 MA correctly

```

### Updating data
```python
while True:
    
    snapshot()
    time.sleep(300)
    print(f'Ran {i} time')
    i = i+1
```

### Building a Custom Watchlist
Build your portfolio by adding the stocks in /long/long.csv in format below

```excel
Tata Chemicals,TATACHEM.NS 
Tata Coffee,TATACOFFEE.NS
```
### Analysis 

#### Analysis technique : Moving Average
```python
    def moving_avg(df):
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean() #for 100 moving avg
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
```
#### Reading and Passing the dataframe.
```python    
    for filename in os.listdir('datasets/long'):
    df = pandas.read_csv('datasets/long/{}'.format(filename))
    vol_break(df)
    moving_avg(df)
```

#### Sending it to Streamlit
```python
    hundredma = pd.DataFrame(ma, columns=['Hundred_MA'])
    twohundredma = pd.DataFrame(tma, columns=['two_Hundred_MA'])

    st.dataframe(hundredma)
    st.dataframe(twohundredma)
```
### Visualizing data
Run the Streamlit server by hitting the commmand

```shell
streamlit run streamapp_500.py
```

