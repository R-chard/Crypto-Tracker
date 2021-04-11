import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime

API_KEY = "e0e92287f03538a81333536881f29373f6313f8fae8093c1526eb53703828f51"

def get_prices(coin):
    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(coin)).json()["DISPLAY"][coin]["USD"]
    data = {
        "ticker": coin,
        "price": crypto_data["PRICE"],
        "change_day": crypto_data["CHANGEDAY"],
        "change_hour": crypto_data["CHANGEHOUR"],
        "market_cap": crypto_data["MKTCAP"],
        "volume_day": crypto_data["VOLUMEDAYTO"],
        "day_open": crypto_data["OPENDAY"],
        "day_high": crypto_data["HIGHDAY"],
        "day_low": crypto_data["LOWDAY"]
    }

    return data

def get_graph_info(rate,coin):
    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/v2/histo{}?fsym={}&tsym=USD&limit=10".format(rate,coin)).json()
    data = {}
    times = []
    price = []
    for i in range(10):
        t = (crypto_data['Data']['Data'][i]['time'])
        timestamp = datetime.datetime.fromtimestamp(t)
        times.append(timestamp)
        price.append(crypto_data['Data']['Data'][i]['close'])

    data['time'] = times
    data['price'] = price
    fig, ax = plt.subplots(figsize=(8, 7))
    plt.xticks(rotation=30)

    plt.title('{} Close prices for the last 10 {}s'.format(coin,rate))
    plt.xlabel('Time')
    if rate == "hour":
        label = "Hourly"
    elif rate == "day":
        label = "Daily"
    elif rate == "minute":
        label = "Minute"
    plt.ylabel('{} Close Prices'.format(label))
    
    plt.plot_date(times, price)
    plt.plot(times,price)

    date_form = DateFormatter("%d-%m %H:%M")
    ax.xaxis.set_major_formatter(date_form)
    path = "graphs/{}.png".format(coin)
    plt.savefig(path)
    
    return path

def get_top_coins(count):
    crypto_coins = requests.get(f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit={count}&tsym=USD").json()["Data"]
    coins = [{} for i in range(int(count))]
    for i in range(len(crypto_coins)):
        data = {
            "ticker": crypto_coins[i]["CoinInfo"]["Name"],
            "name": crypto_coins[i]["CoinInfo"]["FullName"],
            "price": crypto_coins[i]["DISPLAY"]["USD"]["PRICE"],
            "market_cap": crypto_coins[i]["DISPLAY"]["USD"]["MKTCAP"],
            "volume_day": crypto_coins[i]["DISPLAY"]["USD"]["VOLUMEDAYTO"],
            "day_open": crypto_coins[i]["DISPLAY"]["USD"]["OPENDAY"],
            "day_high": crypto_coins[i]["DISPLAY"]["USD"]["HIGHDAY"],
            "day_low": crypto_coins[i]["DISPLAY"]["USD"]["LOWDAY"]
        }
        coins[i] = data

    return coins

