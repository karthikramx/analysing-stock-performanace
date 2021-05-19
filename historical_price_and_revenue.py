import pandas as pd
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    fig.add_trace(
        go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"),
                   name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True),
                             y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


def get_revenue_data(soup):
    revenue_table = soup.find_all("table", {"class": "historical_data_table table"})
    revenue_data = pd.DataFrame(columns=["Date", "Revenue"])
    for row in revenue_table[1].find("tbody").find_all("tr"):
        col = row.find_all("td")
        date = col[0].text
        revenue = col[1].text
        if revenue:
            revenue = revenue.replace('$', '').replace(',', '')
            revenue_data = revenue_data.append({"Date": date, "Revenue": revenue}, ignore_index=True)
    return revenue_data


# tesla historical data
tesla_ticker = yf.Ticker("TSLA")
tesla_hist_data = tesla_ticker.history(period="max")
tesla_hist_data.reset_index(inplace=True)


# tesla revenue data
tesla_hist_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork-23455606&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork-23455606&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork-23455606&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork-23455606&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ"
tesla_page = requests.get(tesla_hist_url)
tesla_soup = BeautifulSoup(tesla_page.content, "html5lib")
tesla_revenue = get_revenue_data(tesla_soup)

# plotting historical share price and revenue
make_graph(tesla_hist_data, tesla_revenue, "Tesla")

print("debug")
