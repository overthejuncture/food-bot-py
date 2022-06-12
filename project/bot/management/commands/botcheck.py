from telegram.ext import Updater
from telegram import Update
import logging
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from bot.models import Choise
from django.core.management.base import BaseCommand
import urllib.parse

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        updater = Updater(token='5496803027:AAHYR1Qp5wI-ooEhMWGkYNB7YnQ89nDpVcg')
        dispatcher = updater.dispatcher

        def start(update: Update, context: CallbackContext):
            choises = Choise.objects.all()
            reply_text = ''
            strings = []
            for idx, choise in enumerate(choises):
                txt = "{idx}. {text}"
                strings.append(reply_text + txt.format(idx=idx+1, text=choise.text))
            if strings:
                update.message.reply_text("\n".join(strings))
            else:
                update.message.reply_text("No data")

        def add(update: Update, context: CallbackContext):
            if not context.args:
                return
            reply_text = ' '.join(context.args)
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

        start_handler = CommandHandler('start', start)
        add_handler = CommandHandler('add', add)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(add_handler)

        updater.start_polling()
