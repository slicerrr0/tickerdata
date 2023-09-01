import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

class StockAnalyzer:
    def get_time(period: int):
        today = datetime.today()
        dif = timedelta(days=period)
        earlier = today - (2 * dif)
        return earlier.strftime("%Y-%m-%d")

    def get_data(symbol: str, period: int):
        symbol = symbol.upper()
        today = datetime.today().strftime('%Y-%m-%d')
        data = yf.download(symbol, start=StockAnalyzer.get_time(period), end=today)
        data = pd.concat([data, pd.DataFrame({'Open': [StockAnalyzer.get_open_price(symbol)], 'Close': [StockAnalyzer.get_current_price(symbol)]})], ignore_index=True)
        return data

    def get_current_price(symbol: str):
        ticker = yf.Ticker(symbol.upper())
        todays_data = ticker.history(period='1d')
        return todays_data['Close'][0]

    def get_open_price(symbol: str):
        ticker = yf.Ticker(symbol.upper())
        todays_data = ticker.history(period='1d')
        return todays_data['Open'][0]

    def get_sma(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        sma = ta.sma(data["Close"], length = period)
        data = data.assign(SMA = sma)
        return data.iloc[-1]['SMA']

    def get_ema(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        ema = ta.ema(data["Close"], length = period)
        data = data.assign(EMA = ema)
        return data.iloc[-1]['EMA']

    def get_rsi(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        rsi = ta.rsi(data["Close"], length=period)
        data = data.assign(RSI = rsi)
        return data.iloc[-1]['RSI']

    def get_stdev(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        stdev = ta.stdev(data["Close"], length=period)
        data = data.assign(STDEV = stdev)
        return data.iloc[-1]['STDEV']

    def get_cumr(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        length = data.shape[0] - 1
        cumrp = (StockAnalyzer.get_current_price(symbol) / data.loc[length - (period - 1), 'Close'])
        return cumrp

    def get_adv(symbol: str, period: int):
        data = StockAnalyzer.get_data(symbol, period)
        length = data.shape[0] - 1 
        first = length - period
        total = 0
        for i in range(first, length):
            total += data.loc[i, 'Close'] * data.loc[i, 'Volume']
        return (total / period) / 1000000

def main():
    signal = input("0. Exit \n1. SMA \n2. EMA \n3. RSI \n4. STDEV \n5. CUMR\n6. ADV\n")
    if signal == "0":
        quit()
    else:
        symbol = input("Enter Ticker \n")
        period = int(input("Enter length \n"))
        if signal == "1":
            print(StockAnalyzer.get_sma(symbol, period))
        elif signal == "2":
            print(StockAnalyzer.get_ema(symbol, period))
        elif signal == "3":
            print(StockAnalyzer.get_rsi(symbol, period))
        elif signal == "4":
            print(StockAnalyzer.get_stdev(symbol, period))
        elif signal == "5":
            print(StockAnalyzer.get_cumr(symbol, period))
        elif signal == "6":
            print(StockAnalyzer.get_adv(symbol, period))

if __name__ == "__main__":
    main()
