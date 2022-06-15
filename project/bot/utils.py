from typing import Union, List
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import json

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

def getKeyboardForChoises(start, limit, choises, show_previous_button):
    buttons = []
    strings = []
    # put this in separate function with params for start and limit
    for idx, choise in enumerate(choises):
        strings.append("{idx} {text}".format(idx=idx+1, text=choise.text))
        buttons.append(
            InlineKeyboardButton(idx+1, callback_data=json.dumps({"id": choise.id}))
        )
    more_buttons = []
    if start > 0:
        more_buttons.append(InlineKeyboardButton("<", callback_data=json.dumps({"start": start - limit, "action":"prev"})))
    if show_previous_button:
        more_buttons.append(InlineKeyboardButton(">", callback_data=json.dumps({"start": start + limit, "action":"next"})))

    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=5,footer_buttons=more_buttons))
    return reply_markup, strings

