import yfinance as yf
import pandas as pd
from get_all_tickers import get_tickers as gt


class Options:
    def generateFinanceObject(self, ticker):
        return yf.Ticker(ticker)

    def getWeeklyOptionChain(self, ticker):
        financeObj = Options.generateFinanceObject(self, ticker)
        dates = financeObj.options
        chain = financeObj.option_chain(dates[0])
        return chain

    def getExpirationDates(self, ticker):
        financeObj = Options.generateFinanceObject(self, ticker)
        return financeObj.options

    def getWeeklyStrikes(self, ticker):
        financeObj = Options.generateFinanceObject(self, ticker)
        dates = financeObj.options
        chain = financeObj.option_chain(dates[0])
        calls = chain.calls[['strike']]
        puts = chain.puts[['strike']]
        combined = pd.concat(
            [calls, puts]).drop_duplicates().reset_index(drop=True)
        combined.sort_values(by=['strike'], inplace=True)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            return combined.to_string(index=False)

    def getAllTickers(self):
        list_of_tickers = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
        return list_of_tickers


obj = Options()

print("Enter Ticker")
ticker = input().upper()

print(obj.getExpirationDates(ticker))
print(obj.getWeeklyOptionChain(ticker))
print(obj.getWeeklyStrikes(ticker))
# print(obj.getAllTickers())


# find most liquid options
# subtract bid from ask and find least one, record every day

# ta lib python library


# return a list of options / tickers that match paramaters

# ATR (average true range)
