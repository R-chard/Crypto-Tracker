import requests
import telegram
import _thread as thread
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from tracker import get_prices, get_top_coins,get_graph_info

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

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

        message = f"Ticker: {ticker}\nCuurent Price: {price}\nHour Change: {change_hour}\nDay Change: {change_day:}\nMarket Cap: {market_cap}\nVolume Traded Today: {volume_day}\nDay Opening Price: {day_open}\nDay High: {day_high}\nDay Low: {day_low}\n\n"

        context.bot.send_message(chat_id=chat_id, text=message)

    except: # request had an error

        context.bot.send_message(chat_id=chat_id, text="The specified coin was not found in our API. Please check that you have the correct Ticker Symbol")

def graph(update, context):
    try:
        chat_id = update.effective_chat.id
        text = update.message.text.split()
        coin = text[2]
        interval = text[1]
        path = get_graph_info(interval,coin)
        context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=chat_id, text="Error while generating graph")

# returns top X coins by market cap
def top(update,context):
    chat_id = update.effective_chat.id

    try:
        coins = get_top_coins(10)
        message = ""
        for coin in coins:
            message +=  f"Name: {coin['name']}\nTicker Symbol: {coin['ticker']}\nCurrent Price: {coin['price']}\nMarket Cap: {coin['market_cap']}\nVolume Traded Today: {coin['volume_day']}\nDay Opening Price: {coin['day_open']}\nDay High: {coin['day_high']}\nDay Low: {coin['day_low']}\n\n"

        context.bot.send_message(chat_id=chat_id,text=message)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id,text="Unknown error. Please try again later")

# polling function to be ran on a seperate thread
def thread_poller(chat_id,context,alert):
    # Time in seconds to delay thread
    DELAY = 60
    count = 0
    # Alert expires after 16hrs
    while count<1000:
        
        coin,isAbove,threshold_price = alert
        data = get_prices(coin)
        currentPrice = float(data["price"][1:].replace(',','')) # First character is the dollar sign
        if isAbove:
            if currentPrice > threshold_price:
                message = f"Price of {data['ticker']} is now at {data['price']} and above your threshold price of ${threshold_price}"
                context.bot.send_message(chat_id=chat_id,text=message)
                break
        elif currentPrice < threshold_price:
            message = f"Price of {data['ticker']} is now at {data['price']} and below your threshold price of ${threshold_price}"
            context.bot.send_message(chat_id=chat_id,text=message)
            break

        count += 1
        time.sleep(DELAY)

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

        alert=(text[1],isAbove,threshold_price)
        thread.start_new_thread(thread_poller,(chat_id,context,alert))
    except Exception:
        context.bot.send_message(chat_id=chat_id,text="Invalid input format")

def help(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    message = f'Hello. Thanks for using the CryptoAlert Bot 🤖 \n\nCommands available:\n/get <coin> -- Retrieve pricing data 💰 for a specific coin\n<coin> -- Ticker symbol of a coin\n\n/top -- Retrieve data for the largest 10 🎖 cyptocurrencies by market cap.\n\n/graph <interval> <coin> -- Plots a line graph 📈 of closing price for a particular coin over 10 counts of the specified interval \n<interval> -- Either "day", "hour" or "minute"\n<coin> -- Ticker symbol of a coin\n\n/alert <coin> <direction> <threshold> -- Sets an alert ⏰ that triggers when the price of the coin crosses the specified threshold \n<coin> -- Ticker symbol of a coin\n<direction> -- Either "above" or "below"\n<threshold> -- Price to cross'
    update.message.reply_text(message)

def showButton(update:Update, context:CallbackContext): 
    keyboard = [
        [
            InlineKeyboardButton("price", callback_data="1"),
            InlineKeyboardButton("data", callback_data="2"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button_click(update:Update, context:CallbackContext):
    query = update.callback_query
    if query.data == "1":
        update.message.reply_text("1")
    if query.data == "2":
        update.message.reply_text("2")


dispatcher.add_handler(CommandHandler("help", help)) # links /start with the start function
dispatcher.add_handler(CommandHandler("get", get)) # links /get with the get function
dispatcher.add_handler(CommandHandler("top", top))
dispatcher.add_handler(CommandHandler("graph", graph))
dispatcher.add_handler(CommandHandler("alert",alert))

updater.dispatcher.add_handler(CallbackQueryHandler(button_click))
updater.start_polling()
updater.idle()