import requests
from twilio.rest import Client

# Stock API
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "OS9Y99ICILR9MOD2"

# News API
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "ddaf147bdfb2494cbf825a828418cd21"

# twilio api
auth_token = "72e9d557741e3d349a6b13801044eae9"
account_sid = "AC1940bb58ee26f57f2ed87c48ccf402d6"
from_num = "+15345444344"
to_num = "+15206390031"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
diff_indicator = None

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}

news_params = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_resp = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_resp.raise_for_status()
stock_data = stock_resp.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

#TODO 1. - Get yesterday's closing stock price. 
yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#TODO 2. - Get the day before yesterday's closing stock price
previous_day_data = stock_data_list[1]
previous_closing_price = previous_day_data["4. close"]

#TODO 3. - Find the abs between 1 and 2.
difference = float(yesterday_closing_price) - float(previous_closing_price)
if difference > 0:
    diff_indicator = "🔺"
else:
    diff_indicator = "🔻"

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round(difference / float(yesterday_closing_price) * 100)

## STEP 2: https://newsapi.org/ 
# Get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - News API to get articles related to the COMPANY_NAME.
if abs(diff_percent) > 5:
    news_resp = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_articles = news_resp.json()["articles"]
    

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    latest_three_articles = news_articles[:3]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
#to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}: {diff_indicator}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in latest_three_articles]

#TODO 9. - Send each article as a separate message via Twilio. 
client = Client(account_sid, auth_token)
for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=from_num,
            to=to_num
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

