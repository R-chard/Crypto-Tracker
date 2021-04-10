import requests


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