import requests as r
import pandas as pd
import json
from pandas.io.json import json_normalize
from datetime import datetime,timedelta
import numpy as np
import math
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import sklearn.linear_model
import matplotlib as pl


def main():    
    '''
    main function
    '''
    menu = ('Get Prices For Available Trading Pairs', 'Predictions', 'Best Chances for Arbitrage', 'Quit')
    while True:
        print("\n")
        print("Arbitrage On Exchanges")
        print("\n")
        print("Find Arbitrage Opportunities for Trading Pairs On Poloniex, Binance, and Bitfinex")
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
           coin_df = get_data()
           all_exchange_list = exchange_list(coin_df)
           ask_price_df, bid_price_df = get_dataframes(all_exchanges_list)
           ask_df = ask_df(ask_price_df)
           bid_df = bid_df(bid_price_df)
           spread_df = spread_df(ask_df, bid_df)
           pair = select_crypto()
           exchange = select_exchange()
           ask, bid = get_prices(exchange, pair)
           print("\n")
           print("The Ask Price for " + pair + " is " + str(ask))
           print("The Bid Price for " + pair + " is " + str(bid))
           print("\n")
        elif choice == 2:
            print("\n")
            predexch = get_predexchange()
            crypto1, crypto2 = pred_crypto()
            print("Getting Prediction for "+crypto1+"-"+crypto2+" on " + predexch)
            ML_df = get_prediction(crypto1, crypto2,predexch)
            forecast_set = get_forecast(ML_df)
            graph = graphs(ML_df, forecast_set)
            print(graph)
            
        elif choice == 3:
            coin_df = get_data()
            all_exchange_list = exchange_list(coin_df)
            ask_price_df, bid_price_df = get_dataframes(all_exchanges_list)
            ask_df = ask_df(ask_price_df)
            bid_df = bid_df(bid_price_df)
            spread_df = spread_df(ask_df, bid_df)
            top_10 = top_10(spread_df)
            print("Arbitrage Opportunities")
            print("\n")
            print(top_10)
        elif choice == 4:
            print("bye")
            
        else:
          print("Not An Option ")
          return
      
def display_menu(menu,exit_option=-1):
    '''
    This function controls the main menu
    '''
    for m in menu:
        print(menu.index(m)+1,".  ",m)
    choice = int(input("Enter choice [1-4]: "))
    if choice==exit_option:
        print("Bye")
        quit()
    return choice

def select_crypto():
    '''
    This function returns the currency that we will get the ask & bid price 
    '''
    print("Trading Pairs Available ")
    pair = ["BCH-BTC", "BCH-ETH","DASH-BTC", "ETC-BTC", "ETH-BTC", "LTC-BTC", "OMG-BTC", "OMG-ETH", "XMR-BTC", "XRP-BTC", "ZEC-BTC", "ZRX-BTC","ZRX-ETH"]

    for p in pair:
        print(pair.index(p)+1,".  ", p)
    crypto = int(input("Please Select Pair to View Price: "))
    item = crypto-1
    pair = pair[item]
    pair = pair.lower().replace('-','')
    return pair 

def select_exchange():
    '''
    This function returns the exchange that we will find the ask & bid price 
   '''
    print("Exchanges Available ")
    exchanges = [x.lower() for x in all_exchanges_list]
    for e in exchanges:
        print(exchanges.index(e)+1,".  ", e)
    exchange = int(input("Please Select an exchange: "))
    item = exchange-1
    exchange = exchanges[item] 
    return exchange

def get_prices(exchange, pair):
    '''
    This function gets the ask & bid function from the above functions.
    '''
    url = "https://coinograph.io/ticker/"
    querystring = {"symbol":exchange+':'+pair}
    header = {'Authorization': 'Token 0800f9d409f84e62642f03490e05e058813ce74f'}
    response = r.request("GET", url, headers=header, params=querystring)
    response = response.text
    parsed = json.loads(response)
    ask = parsed['ask']
    bid = parsed['bid']
    return ask, bid
    
def get_predexchange():
    '''
    This function selects the exchange that we are using to make a prediction
    '''
    exchanges = ['Binance', 'Poloniex', 'Bitfinex']
    for e in exchanges:
        print(exchanges.index(e)+1,".  ", e)
    exchange = int(input("Please Select an Exchange For Prediction: "))
    item = exchange-1
    predexch = exchanges[item] 
    return predexch

def pred_crypto():
    '''
    This function selects the trading pair that we are using to make a prediction
    '''
    pair = ["BCH-BTC", "BCH-ETH","DASH-BTC", "ETC-BTC", "ETH-BTC", "LTC-BTC", "OMG-BTC", "OMG-ETH", "XMR-BTC", "XRP-BTC", "ZEC-BTC", "ZRX-BTC","ZRX-ETH"]
    for p in pair:
        print(pair.index(p)+1,".  ", p)
    crypto = int(input("Please Select Pair to View Prediction: "))
    item = crypto-1
    pair = pair[item]
    crypto1, crypto2 = pair.split('-')
    return crypto1, crypto2 

def get_prediction(crypto1, crypto2,predexch):
    '''
    This function returns the dataframe of information for prediction
    '''
    URL = 'https://min-api.cryptocompare.com/data/histohour?fsym='+crypto1+'&tsym='+crypto2+'&limit=2000&aggregate=1&e='+predexch
    ML = r.get(URL)
    ML = json.loads(ML.text)
    ML_df = json_normalize(ML, record_path = ['Data'],  meta = ['Response','Type','ML','Aggregated'],record_prefix = 'Data_', errors = 'ignore')
    ML_df = pd.DataFrame(ML_df)
    return ML_df
    
    
def get_forecast(ML_df):
    pd.options.mode.chained_assignment = None 
    last= ML_df['Data_close'].iloc[-1]
    df3 = ML_df[['Data_close', 'Data_volumefrom','Data_volumeto']]
    df3['high_change'] = (ML_df['Data_high'].sub(ML_df['Data_close'].shift()).div(ML_df['Data_close'] -1 ).fillna(0))
    df3['price_change'] = (ML_df['Data_close'].sub(ML_df['Data_open'].shift()).div(ML_df['Data_close'] -1 ).fillna(0))    
    forecast_col = 'Data_close'
    df3 = df3[np.isfinite(df3['Data_close'])]
    #Day difference 
    forecast_out = int(math.ceil(0.05*len(df3)))
    df3['label'] = df3[forecast_col].shift(-forecast_out)
    
    X = np.array(df3.drop(['label'],1)) 
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]
  
    df3.dropna(inplace = True)
    Y = np.array(df3['label'])
    #split data into train and test
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size = 0.2)

    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    accuracy = clf.score(X_test, Y_test)
    accuracy
    forecast_set = clf.predict(X_lately)
    return forecast_set
   
   
    
def estimate(avg_forecast,last,crypto1, crypto2, predexch):
    delta = str(avg_forecast - last)
    if avg_forecast > last:
        print(crypto1+' is expected to increase by '+ delta +" "+ crypto2 +' on '+ predexch +' in the next 5 days!')
    else:
        print(crypto1+' is expected to decrease by '+ delta +" "+ crypto2 +' on '+ predexch +' in the next 5 days!')

def graphs(ML_df, forecast_set):
    ML_df = ML_df[np.isfinite(ML_df['Data_close'])]
    df = ML_df
    last_date = pd.to_datetime(df['Data_time'].iloc[-1], unit = 's')
    unix = 3600
    last_unix = last_date.timestamp()
    next_unix = last_unix + unix
    df.set_index('Data_time', inplace=True, drop=True)
    
    df['Forecast'] = np.nan

    for i in forecast_set:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += unix 
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

    df['Forecast'].plot()
    df['Data_close'].plot()
    plt.legend(loc=1)
    plt.title('3 Month View')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()
    
def graphs2(ML_df, forecast_set):
    ML_df = ML_df[np.isfinite(ML_df['Data_close'])]
    df = ML_df.iloc[-336:]
    last_date = pd.to_datetime(df['Data_time'].iloc[-1], unit = 's')
    unix = 3600
    last_unix = last_date.timestamp()
    next_unix = last_unix + unix
    df.set_index('Data_time', inplace=True, drop=True)
    
    df['Forecast'] = np.nan

    for i in forecast_set:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += unix 
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

    df['Forecast'].plot()
    df['Data_close'].plot()
    plt.legend(loc=1)
    plt.title('2 Week View')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()


def get_data():
    url = 'https://rest.coinapi.io/v1/quotes/latest?limit=10000'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    coin = r.get(url, headers=headers)
    data = coin.text
    parsed = json.loads(data)
    coin_df = pd.DataFrame.from_dict(parsed, orient='columns')
    return coin_df

def exchange_list(coin_df):
    all_exchanges_df = coin_df
    all_exchanges_df[['exchange','pair']] = coin_df['symbol_id'].str.split('_', expand=True, n=1)
    all_exchanges_list = ['BINANCE', 'POLONIEX', 'BITFINEX']
    return all_exchanges_list

def get_dataframes(all_exchanges_list):
    exchanges2_df = all_exchanges_df[all_exchanges_df.exchange.isin(all_exchanges_list)]
    ask_price_df = exchanges2_df[['ask_price', 'exchange', 'pair']]
    bid_price_df = exchanges2_df[[ 'bid_price', 'exchange', 'pair']]
    return ask_price_df, bid_price_df

def ask_df(ask_price_df):
    ask_price_df = ask_price_df.drop_duplicates(['exchange','pair'])
    ask_price_df = ask_price_df.pivot(index='pair', columns='exchange')
    ask_price_df = ask_price_df.dropna()
    ask_price_df.columns = ask_price_df.columns.droplevel(0)
    ask_df = ask_price_df.rename_axis(None, axis=1)
    return ask_df

def bid_df(bid_price_df):
    bid_price_df = bid_price_df.drop_duplicates(['exchange','pair'])
    bid_price_df = bid_price_df.pivot(index='pair', columns='exchange')
    bid_price_df = bid_price_df.dropna()
    bid_price_df.columns = bid_price_df.columns.droplevel(0)
    bid_df = bid_price_df.rename_axis(None, axis=1)
    return bid_df

def spread_df(ask_df, bid_df):
    spread_df= pd.DataFrame()
    spread_df["Binance/Bitfinex"] = bid_df.iloc[:,0] - ask_df.iloc[:,1]
    spread_df["Binance/Poloniex"] = bid_df.iloc[:,0] - ask_df.iloc[:,2]
    spread_df["Bitfinex/Binance"] = bid_df.iloc[:,1] - ask_df.iloc[:,0]
    spread_df["Bitfinex/Poloniex"] = bid_df.iloc[:,1] - ask_df.iloc[:,2]
    spread_df["Poloniex/Binance"] = bid_df.iloc[:,2] - ask_df.iloc[:,0]
    spread_df["Poloniex/Bitfinex"] = bid_df.iloc[:,2] - ask_df.iloc[:,1]
    spread_df = spread_df.reset_index()
    return spread_df

def top_10(spread_df):
    spread_df = pd.melt(spread_df, id_vars='pair')
    spread_df.columns = ["Pair", "Exchanges", "Arbitrage Value"]

    top_10 = spread_df.nlargest(10, 'Arbitrage Value')
    top_10 = top_10[(top_10 > 0).all(1)]
    return top_10


if __name__ == "__main__":
    main()
    
