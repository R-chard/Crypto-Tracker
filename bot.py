import requests
import telegram
import _thread as thread
import time
from telegram.ext import Updater, CommandHandler, MessageHandler
from tracker import get_prices, get_top_coins,get_graph_info

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

# chat_id: {coin,isAbove,price}
activeAlerts = {}

def get(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    coin = text.split()[1] # gets type of coin
    try:
        crypto_data = get_prices(coin)
        ticker = crypto_data["ticker"]
        price = crypto_data["price"]
        change_day = crypto_data["change_day"]
        change_hour = crypto_data["change_hour"]
        market_cap = crypto_data["market_cap"]
        volume_day= crypto_data["volume_day"]
        day_open = crypto_data["day_open"]
        day_high= crypto_data["day_high"]
        day_low= crypto_data["day_low"]

        message = f"Ticker: {ticker}\nPrice: {price}\nHour Change: {change_hour}\nDay Change: {change_day:}\nMarket Cap: {market_cap}\nVolume Traded Today:{volume_day}\nOpening Price: {day_open}\nDay High: {day_high}\nDay Low: {day_low}\n\n"

        context.bot.send_message(chat_id=chat_id, text=message)

    except: # request had an error

        context.bot.send_message(chat_id=chat_id, text="Coin not found")

def photo(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    coin = text.split()[1]
    path = get_graph_info(coin)
    context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path

# returns top X coins by market cap
def top(update,context):
    chat_id = update.effective_chat.id

    try:
        coins = get_top_coins(10)
        message = ""
        for coin in coins:
            message +=  f"Name: {coin['name']}\nTicker Symbol: {coin['ticker']}\nCurrent Price: {coin['price']}\nMarket Cap: {coin['market_cap']}\nVolume Traded Today: {coin['volume_day']}\nOpening Price: {coin['day_open']}\nDay High: {coin['day_high']}\nDay Low: {coin['day_low']}\n\n"

        context.bot.send_message(chat_id=chat_id,text=message)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id,text="Error")

# polling function to be ran on a seperate thread
def thread_poller(threadName,context):
    # Time in seconds to delay thread
    DELAY = 5
    global activeAlerts
    while True:
        time.sleep(DELAY)
        for chat_id,(coin,isAbove,threshold_price) in list(activeAlerts.items()):
            data = get_prices(coin)
            currentPrice = float(data["price"][1:].replace(',','')) # First character is the dollar sign
            if isAbove:
                if currentPrice > threshold_price:
                    message = f"Price of {data['ticker']} is now at {data['price']} and above your threshold price of ${threshold_price}"
                    context.bot.send_message(chat_id=chat_id,text=message)
                    del activeAlerts[chat_id]
            elif currentPrice < threshold_price:
                message = f"Price of {data['ticker']} is now at {data['price']} and below your threshold price of ${threshold_price}"
                context.bot.send_message(chat_id=chat_id,text=message)
                del activeAlerts[chat_id]

def alert(update,context):
    chat_id = update.effective_chat.id
    text = update.message.text.split()
    try:
        if text[2].lower() == "above":
            isAbove = True
        elif text[2].lower() == "below":
            isAbove = False
        else:
            raise ValueError
        
        threshold_price = float(text[3])

        activeAlerts[chat_id]=(text[1],isAbove,threshold_price)
        thread.start_new_thread(thread_poller,("T1",context))
    except Exception:
        context.bot.send_message(chat_id=chat_id,text="Invalid input format")

def start(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    update.message.reply_text('hello start') # message shown when user types /start

dispatcher.add_handler(CommandHandler("start", start)) # links /start with the start function
dispatcher.add_handler(CommandHandler("get", get)) # links /get with the get function
dispatcher.add_handler(CommandHandler("top", top))
dispatcher.add_handler(CommandHandler("photo", photo))
dispatcher.add_handler(CommandHandler("alert",alert))
updater.start_polling()