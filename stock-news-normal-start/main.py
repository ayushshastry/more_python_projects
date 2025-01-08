import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

hide_api = 'xxxxxxxxxxxxxxxxxxxxx'

stock_key = hide_api
news_key = hide_api
twilio_sid = hide_api
twilio_auth = hide_api

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_key,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()['Time Series (Daily)']

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]

yesterday_closing_price = yesterday_data['4. close']
print(yesterday_closing_price)

day_before_yest_data = data_list[1]

day_before_yest_closing_price = day_before_yest_data['4. close']
print(day_before_yest_closing_price)


difference = abs(float(yesterday_closing_price) -
                 float(day_before_yest_closing_price))
print(difference)


diff_pct = (difference / float(yesterday_closing_price)) * 100
print(diff_pct)

if diff_pct > 1:
    news_params = {
        "apiKey": news_key,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    articles = news_response.json()["articles"]
    print(articles)

    three_articles = articles[:3]
    print(three_articles)

formatted_articles = [
    f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

client = Client(twilio_sid, twilio_auth)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_="+123455678",
        to="34589687959",
    )
