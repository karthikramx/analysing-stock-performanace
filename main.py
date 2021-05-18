import yfinance as yf
import matplotlib.pyplot as plt

# Analysing Microsoft stock
ms_ticker = yf.Ticker('MSFT')
ms_hist_data = ms_ticker.history(period="max")

# resseting index of data frame
ms_hist_data.reset_index(inplace=True)

# plotting historical open data along time
ms_hist_data.plot(x="Date", y="Open")
plt.show()

# plotting historical dividend data along time
ms_hist_data.plot(x="Date", y="Dividends")
plt.show()

microsoft_info = ms_ticker.info
print("MICROSOFT -  \tSector:{}".format(microsoft_info["sector"]))
print("MICROSOFT -  \tCountry:{}".format(microsoft_info["country"]))
print("MICROSOFT -  \tMAX VOL TRADED:{}".format(ms_hist_data["Volume"].max()))
print("Hello")