import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime


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

    

if __name__ == "__main__":
    get_graph_info("BTC")