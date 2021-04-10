import requests
API_KEY = "e0e92287f03538a81333536881f29373f6313f8fae8093c1526eb53703828f51"

def get_prices(coin):
    # coins = ["BTC", "ETH", "XRP", "LTC", "BCH", "ADA", "DOT", "LINK", "BNB", "XLM"]
    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(coin)).json()["RAW"]
    data = {
        "coin": coin,
        "price": crypto_data[coin]["USD"]["PRICE"],
        "change_day": crypto_data[coin]["USD"]["CHANGEPCT24HOUR"],
        "change_hour": crypto_data[coin]["USD"]["CHANGEPCTHOUR"]
    }

    return data


if __name__ == "__main__":
    print(get_prices())