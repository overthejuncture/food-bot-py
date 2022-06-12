from django.core.management.base import BaseCommand
import logging
import urllib.parse
import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    Updater
)
from bot.models import Choise
from typing import Union, List

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
                txt = "{idx}. {text} {active}"
                strings.append(reply_text + txt.format(idx=idx+1, text=choise.text, active = 'yes' if choise.active else 'no'))
            if strings:
                update.message.reply_text("\n".join(strings))
            else:
                update.message.reply_text("No data")

        def add(update: Update, context: CallbackContext):
            if not context.args:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Нужно ввести текст после команды, например: /add Фуагра со спаржей")
                return
            ch = Choise(text=' '.join(context.args))
            ch.save()
            reply_text = ' '.join(context.args)
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

        def choose(update: Update, context: CallbackContext):
            choises = Choise.objects.all()
            choise = random.choice(choises)
            buttons = [
                InlineKeyboardButton("Да", callback_data="yes")
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
            context.bot.send_message(chat_id=update.effective_chat.id, text=choise.text, reply_markup=reply_markup)
            return 0

        def build_menu(
            buttons: List[InlineKeyboardButton],
            n_cols: int,
            header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
            footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
        ) -> List[List[InlineKeyboardButton]]:
            menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
            if header_buttons:
                menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
            if footer_buttons:
                menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
            return menu

        def check_inactive(update: Update, context: CallbackContext):
            context.bot.send_message(chat_id=update.effective_chat.id, text="afdsafdfa")

        start_handler = CommandHandler('start', start)
        #choose_handler = CommandHandler('choose', choose)
        add_handler = CommandHandler('add', add)
        choose_handler = ConversationHandler(
            entry_points=[CommandHandler('choose', choose)],
            states={
                0: [CallbackQueryHandler(check_inactive)]
            },
            fallbacks=[]
        )
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(choose_handler)
        dispatcher.add_handler(add_handler)

        updater.start_polling()
