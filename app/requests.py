# import requests
# from config import Config
# from .models import Quotes

# quotes_url = Config.QUOTE_URL

# def getQuotes():
#     random_quotes = requests.get(quotes_url)
#     new_quote = random_quotes.json()
#     author = new_quote.get("author")
#     quote = new_quote.get("quote")
#     quote_object = Quotes(author,quote)
#     return quote_object