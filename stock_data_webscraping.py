import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://finance.yahoo.com/quote/AMZN/history?period1=1451606400&period2=1612137600&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html5lib')

tag = soup.title

print(soup.title)

amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text

    amazon_data = amazon_data.append(
        {"Date": date, "Open": Open, "High": high, "Low": low, "Close": close, "Adj Close": adj_close,
         "Volume": volume}, ignore_index=True)

print(amazon_data.head())
amazon_data.set_index("Date", inplace=True)

# what was the open stock price on Jun 01, 2019
print(amazon_data.loc[['Jun 01, 2019'], ['Open']])
print("debug")
