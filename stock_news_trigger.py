import requests
import smtplib

# CONSTANTS:

EMAIL = "ENTER YOUR FROM EMAIL ID"
PASSWORD = "ENTER YOUR PASSWORD"
STOCK = "OLECTRA.BSE" 
COMPANY_NAME = "Olectra Greentech Ltd"
STOCK_PERCENT_CHANGE = 5
NEWS_API_KEY = "ENTER YOUR NEWS API KEY"
NEWS_API_END_POINT = "https://newsapi.org/v2/everything"
NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "searchIn": "title,description",
    "sortBy": "popularity",
    "language": "en",
    "apiKey": NEWS_API_KEY,
}
STOCK_API_KEY = "ENTER YOUR STOCK API KEY"
STOCK_API_END_POINT = "https://www.alphavantage.co/query"
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

# Function for stock trade direction


def symbol(pc):
    if pc > 0:
        return "up"
    else:
        return "down"


# Stock APIS Requests

stock_api = requests.get(STOCK_API_END_POINT, params=STOCK_PARAMETERS)
stock_json = stock_api.json()
previous_close = stock_json["Time Series (Daily)"][list(stock_json["Time Series (Daily)"].keys())[1]]["4. close"]
current_close = stock_json["Time Series (Daily)"][list(stock_json["Time Series (Daily)"].keys())[0]]["4. close"]
price_change = round(float(current_close) - float(previous_close), 2)
percent_change = round(price_change / float(previous_close) * 100, 2)

# News Variables

news_sources = []
news_titles = []
news_desc = []
news_urls = []
news_data = []
news_count = ""

# News Trigger Function


def get_news():
    global news_sources, news_titles, news_desc, news_urls, news_data, news_count
    news_api = requests.get(NEWS_API_END_POINT, params=NEWS_PARAMETERS)
    news_json = news_api.json()
    news_data = news_json["articles"]
    news_count = int(news_json["totalResults"])
    news_sources = [news_data[x]["source"]["name"] for x in range(news_count)]
    news_titles = [news_data[x]["title"] for x in range(news_count)]
    news_desc = [news_data[x]["description"] for x in range(news_count)]
    news_urls = [news_data[x]["url"] for x in range(news_count)]


# Email Tigger Stock logic

if percent_change > STOCK_PERCENT_CHANGE or percent_change < (STOCK_PERCENT_CHANGE * -1):
    get_news()
    email_body = ""
    for n in range(int(news_count)):
        email_body += f"\nArticle {n+1}:\nFrom {news_sources[n]}\nTitle: {news_titles[n]}\nDescription: {news_desc[n]}\n"
        f"Article URL: {news_urls[n]}\n\n"
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=EMAIL,
        to_addrs="stambat4@gmail.com",
        msg=f"Subject:{COMPANY_NAME} Stock Movement {symbol(percent_change)} {percent_change}%\n\n"
            f"\n{email_body}"
            f"\n\nHappy Investing!!!")
    connection.close()
