from queue import Empty
from django.core.management.base import BaseCommand
import logging
import urllib.parse
import random
import json

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

        def list_choises(update: Update, context: CallbackContext):
            inactive_choises = Choise.objects.filter(active=False)
            active_choises = Choise.objects.filter(active=True)
            reply_text = "Активные варианты:\n"
            strings = []
            for idx, choise in enumerate(active_choises):
                txt = "{idx}. {text}"
                strings.append(txt.format(idx=idx+1, text=choise.text, active = 'yes' if choise.active else 'no'))
            if strings:
                reply_text = reply_text + "\n".join(strings)
            else:
                reply_text = reply_text + "-"
            reply_text = reply_text + "\n\nНеактивные варианты:\n"
            strings = []
            for idx, choise in enumerate(inactive_choises):
                txt = "{idx}. {text}"
                strings.append(txt.format(idx=idx+1, text=choise.text, active = 'yes' if choise.active else 'no'))
            if strings:
                reply_text = reply_text + "\n".join(strings)
            else:
                reply_text = reply_text + "-"

            update.message.reply_text(reply_text)
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
                InlineKeyboardButton("Да", callback_data=json.dumps({'id': choise.id, 'text':"yes"})),
                InlineKeyboardButton("Нет", callback_data=json.dumps({'id': choise.id, 'text':"no"}))
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
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
            update.callback_query.edit_message_reply_markup(None)
            data = json.loads(update.callback_query.data)
            if data.get('text') == 'yes':
                #set inactive
                choise = Choise.objects.get(pk=data.get('id'))
                choise.active = False
                choise.save()
                context.bot.send_message(chat_id=update.effective_chat.id, text="Рецепт добавлен в неактивные")
            return ConversationHandler.END

        def reset_inactive(update: Update, context: CallbackContext):
            inactive = Choise.objects.filter(active=False)
            for choise in inactive:
                choise.active=True
                #todo bulk_update
                choise.save()
            update.message.reply_text("Список неактивных рецептов был очищен")
            
        def check(update: Update, context: CallbackContext):
            limit = 3
            start = 0
            update_message = False

            # if id in callback then send new message

            if update.callback_query:
                print('callback')
                update_message = True
                #context.bot.send_message(chat_id=update.effective_chat.id, text=update.callback_query.data)
                data = json.loads(update.callback_query.data)
                if data["action"] and data["action"] == 'next':
                    start = data['start']
                elif data["action"] and data["action"] == 'prev':
                    start = data['start'] if int(data['start']) > 0 else 0
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="no data")

            print("start: {start}".format(start=start))
            choises = Choise.objects.all()[start:start + limit]
            if not choises.exists():
                return 0
            buttons = []
            strings = []
            for idx, choise in enumerate(choises):
                strings.append("{idx} {text}".format(idx=idx+1, text=choise.text))
                buttons.append(
                    InlineKeyboardButton(idx+1, callback_data=choise.id)
                )
            more_buttons = [
            ]
            if start > 0:
                more_buttons.append(InlineKeyboardButton("Previous", callback_data=json.dumps({"start": start - limit, "action":"prev"})))
            if Choise.objects.all()[start + limit:start + limit + 1]:
                more_buttons.append(InlineKeyboardButton("Next", callback_data=json.dumps({"start": start + limit, "action":"next"})))

            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2,footer_buttons=more_buttons))
            if update_message:
                update.callback_query.edit_message_text(text="\n".join(strings), reply_markup=reply_markup)
                return 1
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(strings),
                    reply_markup=reply_markup )
                return 0

        def choise_actions(update: Update, context: CallbackContext):
            buttons = []
            id = update.callback_query.data
            #get chosen option through callback
            context.bot.send_message(chat_id=update.effective_chat.id, text=id)
            #show actions for chosen option
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
            context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup)
            pass

        list_handler = CommandHandler('list', list_choises)
        # redo
        check_handler = ConversationHandler(
            entry_points=[CommandHandler('check', check)],
            states={
                0: [CallbackQueryHandler(check)]
            },
            fallbacks=[]
        )
        #choose_handler = CommandHandler('choose', choose)
        add_handler = CommandHandler('add', add)
        reset_inactive_handler = CommandHandler('reset_inactive', reset_inactive)
        choose_handler = ConversationHandler(
            entry_points=[CommandHandler('choose', choose)],
            states={
                0: [CallbackQueryHandler(check_inactive)]
            },
            fallbacks=[]
        )
        dispatcher.add_handler(list_handler)
        dispatcher.add_handler(reset_inactive_handler)
        dispatcher.add_handler(choose_handler)
        dispatcher.add_handler(check_handler)
        dispatcher.add_handler(add_handler)

        updater.start_polling()
