import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime

API_KEY = "e0e92287f03538a81333536881f29373f6313f8fae8093c1526eb53703828f51"

def get_prices(coin):
    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(coin)).json()["RAW"]
    data = {
        "coin": coin,
        "price": crypto_data[coin]["USD"]["PRICE"],
        "change_day": crypto_data[coin]["USD"]["CHANGEPCT24HOUR"],
        "change_hour": crypto_data[coin]["USD"]["CHANGEPCTHOUR"]
    }

    return data

def get_graph_info(coin):
    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym=USD&limit=10&api_key=e0e92287f03538a81333536881f29373f6313f8fae8093c1526eb53703828f51".format(coin)).json()
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

    plt.title('Last 10 day close prices for {}'.format(coin))
    plt.xlabel('Time')
    plt.ylabel('Hourly Close Price')
    
    plt.plot_date(times, price)
    plt.plot(times,price)

    date_form = DateFormatter("%d-%m %H")
    ax.xaxis.set_major_formatter(date_form)
    plt.show()
    path = "graphs/{}.png".format(coin)
    plt.savefig(path)
    
    return path

def get_top_coins(count):
    crypto_coins = requests.get(f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit={count}&tsym=USD").json()["Data"]
    coins = [{} for i in range(int(count))]
    for i in range(len(crypto_coins)):
        data = {
            "token": crypto_coins[i]["CoinInfo"]["Name"],
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

if __name__ == "__main__":
    get_graph_info("BTC")
