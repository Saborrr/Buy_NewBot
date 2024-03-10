from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonText:
    """Наименования кнопок."""
    HELLO = "Привет!"
    WHATS_NEXT = "Что дальше?"
    BYE = "До свидания!"
    NEED_IT = "Оно мне надо?"


def get_new_start_kb():
    """Схема расположения кнопок."""
    button_hello = KeyboardButton(text=ButtonText.HELLO)
    button_help = KeyboardButton(text=ButtonText.WHATS_NEXT)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    button_need_it = KeyboardButton(text=ButtonText.NEED_IT)
    buttons_row_first = [button_hello, button_help, button_need_it]
    buttons_row_second = [button_bye]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_row_first,
                  buttons_row_second],
        resize_keyboard=True,
        one_time_keyboard=True)
    return markup
