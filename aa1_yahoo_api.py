import yfinance as yf
import matplotlib.pyplot as plt
#data = yf.download('^GDAXI','2016-01-01','2019-08-01')
data = yf.download('^GDAXI','2016-01-01')
#%matplotlib inline
print(data)
print(data['Adj Close'])
data['Adj Close'].plot()
plt.show()
data['Volume'].plot()
plt.show()

msft = yf.Ticker("^GDAXI")
hist = msft.history(period="max")
hist2 = msft.splits
print("splits: "+hist2)
#hist2 = msft.recommendations
# get stock info
hist3 = msft.info
print("info: "+str(hist3))
# get historical market data
hist = msft.history(period="max")
print("history: "+str(hist))

# show actions (dividends, splits)
hist3 = msft.actions
print("actions: "+str(hist3))

# show dividends
hist3 = msft.dividends
print("dividends: "+str(hist3))

# show splits
hist3 = msft.splits
print("splits: "+str(hist3))

# show financials
hist3 = msft.financials
print("financials: "+str(hist3))

hist3 = msft.quarterly_financials
print("quarterly_financials: "+str(hist3))

# show major holders
#stock.major_holders

hist3 = msft.actions
print("actions: "+str(hist3))


