# Data602_Final

Team Members: 
Mike Gankhuyag (Team Lead) and Natalie Mollaghan 

Overview:
There are currently 191 cryptocurrency exchanges throughout the world. Cryptocurrency markets lack the unified infrastructure of more advanced markets that supports this kind of complex trading.  

The large number of exchange choices presents a multitude of problems, since they are unregulated and and disjoined, including a large distribution of prices across the multiple platforms. This presents an opportunity for arbitrage with the different exchanges. 

Proposal:
Our proposal is to explore the bid and ask prices of top cryptocurrencies among various exchanges that offer public api to find negative spread. If we are able to find a negative spread we can explore what a possible profit one might make from buying on one exchange and selling on another. We will consider trading volume and fees to determine if the trade is suitable to make a profit. The result of our project will be a script that compares current prices of cryptocurrencies and if it finds an opportunity for arbitrage, execute an exchange. 

Data Sources:
We will be focusing on the top 10 exchanges to look for arbitrage opportunities, for example:

https://poloniex.com/ 
https://www.kraken.com/ 
Gemini.com 
Coinbase.com (GDAX) 
Binance.com
Kucoin.com
Cryptopia.co.nz


Risks:
Trades need to be as close to real time as possible.
Rest API call rates can limit our actions
Fees might minimize profit on the exchange
The volatility of coin prices
