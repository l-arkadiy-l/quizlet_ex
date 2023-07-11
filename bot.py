from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ParseMode, Message
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import openpyxl
import sqlite3
from excel_parse import go
from translator import *

TOKEN = "6218562911:AAGmPjJYvxMnjOpY3-eyzK37oQrqKSsPzCI"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard_crypto = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
quantity_of_words = 5


def get_users_file(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # c.execute("CREATE TABLE users (id integer UNIQUE, path text)")
    try:
        c.execute(f"INSERT INTO users VALUES ({user_id}, 'pathxl/{user_id}.xlsx')")
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    c.execute(f"SELECT * FROM users WHERE id={user_id}")
    file = c.fetchone()[-1]
    c.close()
    return file


def is_open(file: str) -> bool:
    try:
        f = open(file)
    except FileNotFoundError:
        return False
    return True


# /info - подробный план как пользоватья (сделать в качестве картинок)
@dp.message_handler(commands=['start'])
async def main(message):
    await bot.send_message(message.chat.id,
                           'Hi, I will help you import words with translation to Quizlet or other apps! We hame commands:\n'
                           '/set your number\n'
                           '/info\n'
                           '/set_delimeter your delimeter (by default, it is //)\n'
                           '/add your words (example: /add cat, dog, town, light)\n'
                           '/change_language <- Измените язык, чтобы перейти на русский')


@dp.message_handler(commands=['set'])
async def user_input(message):
    try:
        quantity_of_words = int(message.text.split()[-1])
        await message.reply(f"You chose {quantity_of_words} words")
        await message.reply('Ok, now send me your .xlsx file :0')
    except ValueError:
        await message.reply(f"Error -> Enter one space and one number! Example:\n/set 6")


@dp.message_handler(commands=['add'])
async def user_input(message):
    words = ''.join(message.text.split()[1:]).split(',')
    file_user = f'pathxl/{message.from_user.id}.xlsx'
    eng_file = rf'{file_user}'
    wb = openpyxl.load_workbook(eng_file)
    sheet = wb.active
    # O(n) -> n - count of our words in A column
    last_coord = 0
    list_empty_coords = []
    for row in sheet.iter_rows(min_row=1, min_col=1, max_col=1):
        for cell in row:
            if cell.value is None:
                print(str(cell.row))
                list_empty_coords.append(cell.row)
            last_coord = cell.coordinate[1:]
    n = len(words)
    for i in range(min(len(list_empty_coords), n)):
        sheet[f'A{list_empty_coords[i]}'] = words[0]
        words.pop(0)
    last_coord = int(last_coord) + 1
    n = len(words)
    for i in range(last_coord, last_coord + n):
        sheet[f'A{i}'] = words[0]
        words.pop(0)
    wb.save(file_user)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: Message):
    """func to download xlsx files"""
    user_id = message.from_user.id
    user_file = get_users_file(user_id)
    if is_open(user_file):
        pass
    else:
        wb = openpyxl.Workbook()
        wb.save(user_file)
    # спросить у пользователя хочет ли он изменить файл или оставить текущий (при изменении файл pathxl/user_id перезаписывается)
    if document := message.document:
        await document.download(
            destination_file="english.xlsx"
        )

    added_words, error_words = go('english.xlsx', quantity_of_words)
    await message.reply_document(open('english.xlsx', 'rb'))
    final_text = ''
    for key, item in added_words.items():
        final_text += key + '//' + item + '\n'
    await bot.send_message(message.from_user.id, final_text)


@dp.message_handler(content_types=['text'])
async def user_input(message):
    await bot.send_message(message.from_user.id, "Sorry but I can't to understand you, try to enter other commands")


executor.start_polling(dp)
