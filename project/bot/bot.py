from telegram.ext import Updater
from telegram import Update
import logging
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from models import Choise

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='5496803027:AAHYR1Qp5wI-ooEhMWGkYNB7YnQ89nDpVcg')
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="1334I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
