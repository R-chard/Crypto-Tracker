import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from tracker import get_prices

telegram_bot_token = "1710250957:AAHpexQYf2Sp3aFOoeXmuQbEe0opwA9F9Dw"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
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
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


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