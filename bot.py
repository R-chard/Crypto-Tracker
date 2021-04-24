import requests
import telegram
import _thread as thread
import time
from telegram.ext import *
from telegram import *
from tracker import get_prices, get_top_coins,get_graph_info

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"
bot = Bot(telegram_bot_token)
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
text = ""
MAX_ALERT_LIMIT = 1000
alerts_count = 0

def get(update, context):
    global text
    chat_id = update.effective_chat.id
    text = update.message.text
    coin = text.split()[1] # gets type of coin
    try:
        message = f"Ticker: {coin}"
        keyboard = [
            [
                InlineKeyboardButton("Price", callback_data="price"),
                InlineKeyboardButton("Hour Change", callback_data="hourChange"),
            ],
            [
                InlineKeyboardButton("Day Change", callback_data="dayChange"),
                InlineKeyboardButton("Market Cap", callback_data="marketCap"),
            ],
            [
                InlineKeyboardButton("Volume Traded Today", callback_data="volumeTraded"),
                InlineKeyboardButton("Day Opening Price", callback_data="dayOpening"),
                
            ],
            [
                InlineKeyboardButton("Day High", callback_data="dayHigh"),
                InlineKeyboardButton("Day Low", callback_data="dayLow"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.send_message(chat_id=chat_id, text=message)
        update.message.reply_text('Please choose the data you are interested in:', reply_markup=reply_markup)

    except: # request had an error

        context.bot.send_message(chat_id=chat_id, text="The specified coin was not found in our API. Please check that you have the correct ticker symbol")

def graph(update, context):
    global text
    text = update.message.text
    try:
        chat_id = update.effective_chat.id
        text = update.message.text
        coin = text.split()[1] # gets type of coin
        keyboard = [
            [
                InlineKeyboardButton("Minute", callback_data="min"),
                InlineKeyboardButton("Hour", callback_data="hour"),
                InlineKeyboardButton("Day", callback_data="day"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose the interval:', reply_markup=reply_markup)

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
    while True:
        
        coin,isAbove,threshold_price = alert
        data = get_prices(coin)
        currentPrice = float(data["price"][1:].replace(',','')) # First character is the dollar sign
        if isAbove:
            if currentPrice > threshold_price:
                message = f"Price of {data['ticker']} is now at {data['price']} and above your threshold price of ${threshold_price}"
                context.bot.send_message(chat_id=chat_id,text=message)
                context.bot.send_message(chat_id=chat_id,text="Alert removed from the system")
                break
        elif currentPrice < threshold_price:
            message = f"Price of {data['ticker']} is now at {data['price']} and below your threshold price of ${threshold_price}"
            context.bot.send_message(chat_id=chat_id,text=message)
            context.bot.send_message(chat_id=chat_id,text="Alert removed from the system")
            break

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
        if alerts_count + 1 < MAX_ALERT_LIMIT:
            alerts_count += 1
            context.bot.send_message(chat_id= chat_id, text= "Alert successfully set")
            thread.start_new_thread(thread_poller,(chat_id,context,alert))
        else:
            context.bot.send_message(chat_id= chat_id, text= "There are too many alerts currently running on the system. Please try again later")
        
    except Exception:
        context.bot.send_message(chat_id=chat_id,text="Invalid input format")

def help(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    message = f'Hello. Thanks for using the CryptoAlert Bot 🤖 \n\nCommands available:\n/get <coin> -- Retrieve pricing data 💰 for a specific coin\n<coin> -- Ticker symbol of a coin\n\n/top -- Retrieve data for the largest 10 🎖 cyptocurrencies by market cap.\n\n/graph <coin> -- Plots a line graph 📈 of closing price for a particular coin over 10 counts of the selected interval \n<coin> -- Ticker symbol of a coin\n\n/alert <coin> <direction> <threshold> -- Sets an alert ⏰ that triggers when the price of the coin crosses the specified threshold \n<coin> -- Ticker symbol of a coin\n<direction> -- Either "above" or "below"\n<threshold> -- Price to cross'
    update.message.reply_text(message)


def button_click(update, context):
    query : CallbackQuery = update.callback_query
    chat_id = update.effective_chat.id
    
    coin = text.split()[1]
    crypto_data = get_prices(coin)

    if query.data == "price":
        message = f"Price is: {crypto_data['price']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "hourChange":
        message = f"Hourly Change is: {crypto_data['change_hour']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "dayChange":
        message = f"Daily Change is: {crypto_data['change_day']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "marketCap":
        message = f"Market Cap is: {crypto_data['market_cap']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "volumeTraded":
        message = f"Volume Traded Today is: {crypto_data['volume_day']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "dayOpening":
        message = f"Day Opening Price is: {crypto_data['day_open']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "dayHigh":
        message = f"Day High: {crypto_data['day_high']}"
        context.bot.send_message(chat_id=chat_id, text=message)
    elif query.data == "dayLow":
        message = f"Day Low: {crypto_data['day_low']}"
        context.bot.send_message(chat_id=chat_id, text=message)

    if query.data == "min":
        path = get_graph_info("minute",coin)
        context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path
    if query.data == "hour":
        path = get_graph_info("hour",coin)
        context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path
    if query.data == "day":
        path = get_graph_info("day",coin)
        context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path


dispatcher.add_handler(CommandHandler("help", help)) # links /start with the start function
dispatcher.add_handler(CommandHandler("get", get)) # links /get with the get function
dispatcher.add_handler(CommandHandler("top", top))
dispatcher.add_handler(CommandHandler("graph", graph))
dispatcher.add_handler(CommandHandler("alert",alert))

updater.dispatcher.add_handler(CallbackQueryHandler(button_click))
updater.start_polling()
updater.idle()