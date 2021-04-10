import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
from tracker import get_prices, get_graph_info

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def get(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    print("got text message:", text)
    coin = text.split()[1] # gets type of coin
    try:
        crypto_data = get_prices(coin)
        coin = crypto_data["coin"]
        price = crypto_data["price"]
        change_day = crypto_data["change_day"]
        change_hour = crypto_data["change_hour"]
        message = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

        context.bot.send_message(chat_id=chat_id, text=message)

    except: # request had an error

        context.bot.send_message(chat_id=chat_id, text="Coin not found")

def photo(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    coin = text.split()[1]
    path = get_graph_info(coin)
    context.bot.send_photo(chat_id, photo=open(path, 'rb')) # sends a photo according to path


def start(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    update.message.reply_text('hello start') # message shown when user types /start

dispatcher.add_handler(CommandHandler("start", start)) # links /start with the start function
dispatcher.add_handler(CommandHandler("get", get)) # links /get with the get function
dispatcher.add_handler(CommandHandler("photo", photo))
updater.start_polling()