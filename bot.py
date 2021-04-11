import telegram
<<<<<<< Updated upstream
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from tracker import get_prices
=======
import _thread as thread
import time
from telegram.ext import *
from telegram import *
from tracker import get_prices, get_top_coins,get_graph_info
>>>>>>> Stashed changes

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"
bot = Bot(telegram_bot_token)
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

<<<<<<< Updated upstream
=======
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

        # message = f"Ticker: {ticker}\nCuurent Price: {price}\nHour Change: {change_hour}\nDay Change: {change_day:}\nMarket Cap: {market_cap}\nVolume Traded Today: {volume_day}\nDay Opening Price: {day_open}\nDay High: {day_high}\nDay Low: {day_low}\n\n"
        message = f"Ticker: {ticker}"
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

        context.bot.send_message(chat_id=chat_id, text="Coin not found")

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
>>>>>>> Stashed changes

def start(update, context):
    chat_id = update.effective_chat.id
<<<<<<< Updated upstream
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)
    
def bot(update: Update, context: CallbackContext) -> None:
=======

    try:
        coins = get_top_coins(10)
        message = ""
        for coin in coins:
            message +=  f"Name: {coin['name']}\nTicker Symbol: {coin['ticker']}\nCurrent Price: {coin['price']}\nMarket Cap: {coin['market_cap']}\nVolume Traded Today: {coin['volume_day']}\nDay Opening Price: {coin['day_open']}\nDay High: {coin['day_high']}\nDay Low: {coin['day_low']}\n\n"

        context.bot.send_message(chat_id=chat_id,text=message)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id,text="Error")

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
                break
        elif currentPrice < threshold_price:
            message = f"Price of {data['ticker']} is now at {data['price']} and below your threshold price of ${threshold_price}"
            context.bot.send_message(chat_id=chat_id,text=message)
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
        thread.start_new_thread(thread_poller,(chat_id,context,alert))
    except Exception:
        context.bot.send_message(chat_id=chat_id,text="Invalid input format")

def help(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    message = f'Hello. Thanks for using the CryptoAlert Bot 🤖 \n\nCommands available:\n/get <coin> -- Retrieve pricing data 💰 for a specific coin\n<coin> -- Ticker symbol of a coin\n\n/top -- Retrieve data for the largest 10 🎖 cyptocurrencies by market cap.\n\n/graph <interval> <coin> -- Plots a line graph 📈 of closing price for a particular coin over 10 counts of the specified interval \n<interval> -- Either "day", "hour" or "minute"\n<coin> -- Ticker symbol of a coin\n\n/alert <coin> <direction> <threshold> -- Sets an alert ⏰ that triggers when the price of the coin crosses the specified threshold \n<coin> -- Ticker symbol of a coin\n<direction> -- Either "above" or "below"\n<threshold> -- Price to cross'
    update.message.reply_text(message)
    keyboard = [
        [
            InlineKeyboardButton("price", callback_data="1"),
            InlineKeyboardButton("data", callback_data="2"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def showButton(update:Update, context:CallbackContext): 
>>>>>>> Stashed changes
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

<<<<<<< Updated upstream
=======
def button_click(update:Update, context:CallbackContext):
    query : CallbackQuery = update.callback_query
    chat_id = update.effective_chat.id
    text = update.message.text
    message = f"hello"
    if query.data == "1":
        context.bot.send_message(chat_id=chat_id, text=message)
    if query.data == "2":
        print("two")


dispatcher.add_handler(CommandHandler("help", help)) # links /start with the start function
dispatcher.add_handler(CommandHandler("get", get)) # links /get with the get function
dispatcher.add_handler(CommandHandler("top", top))
dispatcher.add_handler(CommandHandler("graph", graph))
dispatcher.add_handler(CommandHandler("alert",alert))
>>>>>>> Stashed changes

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = update.effective_chat.id
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    
    # Now u can define what choice ("callback_data") do what like this:
    if choice == '1':
        func1()

    if choice == '2':
        func2()

def func1(update, context):
    update.message.reply_text('one')

def func2(update, context):
    update.message.reply_text('two')

def main() -> None:
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("bot", bot))
dispatcher.add_handler(CommandHandler("one", func1))
updater.start_polling()