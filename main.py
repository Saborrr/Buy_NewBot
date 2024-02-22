import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import logging
import os
import sqlite3


load_dotenv()

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot=bot)


conn = sqlite3.connect('orders.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
               (id_order INTEGER PRIMARY KEY AUTOINCREMENT,
               id_username INTEGER,
               file_id TEXT,
               quantity INTEGER,
               size TEXT,
               description TEXT,
               price INTEGER,
               data_order DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S',
               'now', 'localtime')))
               ''')
conn.commit()


def get_new_start_kb():
    button_1 = KeyboardButton(text="Привет!")
    button_2 = KeyboardButton(text="Что дальше?")
    buttons_row_first = [button_1]
    buttons_row_second = [button_2]
    markup = ReplyKeyboardMarkup(keyboard=[buttons_row_first,
                                           buttons_row_second],
                                 resize_keyboard=True)
    return markup


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (f'{message.from_user.full_name}, приветствуем Вас 😊\n'
            'Для начала, отправьте изображение товара 📷')
    await message.answer(text=text,
                         reply_markup=get_new_start_kb(),)






@dp.message(F.photo, ~F.caption)
async def handle_photo(message: types.Message):
    """Функция приема изображения."""
    # отправляет статус "Загрузка фото"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    file_id = message.photo[-1].file_id
    id_username = message.from_user.full_name
    # Записываем информацию о заказе в базу данных
    cursor.execute("INSERT INTO orders (id_username, file_id) VALUES (?, ?)", (
        id_username,
        file_id,
        ))
    conn.commit()
    text = "Изображение товара успешно загружено!\nВведите количество товара:"
    await message.answer(text=text)


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = "Для получения помощи напишите сюда:\n @aa_fdv"
    await message.answer(text=text)


@dp.message()
async def answer(message: types.Message):
    await message.reply('Простите, такой команды нет.')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
