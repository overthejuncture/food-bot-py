import logging
import urllib.parse
import random
import json
from xml.sax.handler import ContentHandler
from bot import utils

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
from bot.models import (
    Choise,
    User
)
from typing import Union, List

def start_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token='5496803027:AAHYR1Qp5wI-ooEhMWGkYNB7YnQ89nDpVcg')
    dispatcher = updater.dispatcher

    list_handler = CommandHandler('list', list_choises)
    start_handler = CommandHandler('start', start)
    # redo
    check_handler = ConversationHandler(
        entry_points=[CommandHandler('check', check)],
        states={
            0: [CallbackQueryHandler(choise_actions)],
            1: [CallbackQueryHandler(action)],
        },
        fallbacks=[],
        allow_reentry=True
    )
    #choose_handler = CommandHandler('choose', choose)
    add_handler = CommandHandler('add', add)
    reset_inactive_handler = CommandHandler('reset_inactive', reset_inactive)
    choose_handler = ConversationHandler(
        entry_points=[CommandHandler('choose', choose)],
        states={
            0: [CallbackQueryHandler(check_inactive)]
        },
        fallbacks=[],
        allow_reentry=True,
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)
    dispatcher.add_handler(reset_inactive_handler)
    dispatcher.add_handler(choose_handler)
    dispatcher.add_handler(check_handler)
    dispatcher.add_handler(add_handler)

    updater.start_polling()

def start(update: Update, context: CallbackContext):
    id = update.message.from_user.id
    update.message.reply_text(update.message.from_user.id)
    if not User.objects.filter(telegram_id=id).exists():
        user = User(telegram_id=id)
        user.save()
        update.message.reply_text('???????? ????????????')

def list_choises(update: Update, context: CallbackContext):
    user = User.objects.get(telegram_id=update.message.from_user.id)
    
    inactive_choises = user.choises.filter(active=False)
    active_choises = user.choises.filter(active=True)

    reply_text = "???????????????? ????????????????:\n"
    strings = []
    for idx, choise in enumerate(active_choises):
        txt = "{idx}. {text}"
        strings.append(txt.format(idx=idx+1, text=choise.text, active = 'yes' if choise.active else 'no'))
    reply_text = reply_text + "\n".join(strings) if strings else reply_text + "-"

    reply_text = reply_text + "\n\n???????????????????? ????????????????:\n"
    strings = []
    for idx, choise in enumerate(inactive_choises):
        txt = "{idx}. {text}"
        strings.append(txt.format(idx=idx+1, text=choise.text, active = 'yes' if choise.active else 'no'))
    reply_text = reply_text + "\n".join(strings) if strings else reply_text + "-"

    update.message.reply_text(reply_text)

def add(update: Update, context: CallbackContext):
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id, text="?????????? ???????????? ?????????? ?????????? ??????????????, ????????????????: /add ???????????? ???? ??????????????")
        return
    ch = Choise(text=' '.join(context.args))
    ch.save()
    user = User.objects.get(telegram_id=update.message.from_user.id)
    user.choises.add(ch)
    reply_text = ' '.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text="???????????????? ??????????????: \"" + reply_text + "\"")

def choose(update: Update, context: CallbackContext):
    user = User.objects.get(telegram_id=update.message.from_user.id)
    choises = user.choises.all()
    if not choises:
        update.message.reply_text('?????? ??????????????????')
        return ConversationHandler.END
    choise = random.choice(choises)
    buttons = [
        InlineKeyboardButton("????", callback_data=json.dumps({'id': choise.id, 'text':"yes"})),
        InlineKeyboardButton("??????", callback_data=json.dumps({'id': choise.id, 'text':"no"}))
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(buttons, n_cols=2))
    context.bot.send_message(chat_id=update.effective_chat.id, text=choise.text, reply_markup=reply_markup)
    return 0

def check_inactive(update: Update, context: CallbackContext):
    update.callback_query.edit_message_reply_markup(None)
    data = json.loads(update.callback_query.data)
    if data.get('text') == 'yes':
        #set inactive
        choise = Choise.objects.get(pk=data.get('id'))
        choise.active = False
        choise.save()
        context.bot.send_message(chat_id=update.effective_chat.id, text="???????????? ???????????????? ?? ????????????????????")
    return ConversationHandler.END

def reset_inactive(update: Update, context: CallbackContext):
    user = User.objects.get(telegram_id=update.message.from_user.id)
    inactive = user.choises.filter(active=False)
    for choise in inactive:
        choise.active=True
        #todo bulk_update
        choise.save()
    update.message.reply_text("???????????? ???????????????????? ???????????????? ?????? ????????????")
    
def check(update: Update, context: CallbackContext):
    start = 0
    limit = 10

    user = User.objects.get(telegram_id=update.message.from_user.id)
    choises = user.choises.all()[start:start + limit]

    show_previous_button = user.choises.all()[start + limit:start + limit + 1]
    reply_markup, strings = utils.getKeyboardForChoises(start, limit, choises, bool(show_previous_button))

    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(strings) if strings else "-",
            reply_markup=reply_markup )
    return 0

def choise_actions(update: Update, context: CallbackContext):
    data = json.loads(update.callback_query.data)
    if 'action' in data:
        return next_and_prev(update, context)

    if 'id' in data:
        return show_choise_actions(update, context)

def next_and_prev(update: Update, context: CallbackContext):
    limit = 10
    data = json.loads(update.callback_query.data)
    start = data['start']

    user = User.objects.get(telegram_id=update.callback_query.from_user.id)
    choises = user.choises.all()[start:start + limit]
    show_previous_button = user.choises.all()[start + limit:start + limit + 1]
    reply_markup, strings = utils.getKeyboardForChoises(data['start'], limit, choises, show_previous_button)
    update.callback_query.edit_message_text("\n".join(strings), reply_markup=reply_markup)
    pass

def show_choise_actions(update: Update, context: CallbackContext):
    update.callback_query.edit_message_reply_markup()
    data = json.loads(update.callback_query.data)
    choise = Choise.objects.get(pk=data['id'])
    buttons = [
        InlineKeyboardButton(text="??????????????", callback_data=json.dumps({'id': choise.id, 'action': 'remove'}))
        # InlineKeyboardButton(text="????????????????", callback_data=json.dumps({'id': choise.id, 'action': 'edit'}))
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(buttons, n_cols=5))
    update.callback_query.bot.send_message(update.callback_query.message.chat_id, choise.text, reply_markup=reply_markup)
    return 1

def action(update: Update, context: CallbackContext):
    update.callback_query.edit_message_reply_markup()
    data = json.loads(update.callback_query.data)
    if data['action'] == 'remove':
        choise = Choise.objects.get(pk=data['id'])
        choise.delete()
        update.callback_query.message.reply_text('??????????????')
    pass
