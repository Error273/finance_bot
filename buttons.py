from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.add(KeyboardButton('Добавить расход'), KeyboardButton('Добавить доход'), KeyboardButton('Статистика'))
