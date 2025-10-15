import yfinance as yf

ticker_symbol = "NOKIA.HE"

ticker = yf.Ticker(ticker_symbol)
hist = ticker.history(period="1d")
print(hist)


print('Financials: \n')
print(ticker.financials)


