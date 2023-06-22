from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from buttons import *

from config import *

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply(
        'Приветствую вас в боте для учета ваших финансов. Здесь вы можете контролировать ваши доходы и расходы!',
        reply_markup=main_kb)


@dp.message_handler()
async def main(msg: types.Message):
    text = msg.text
    if text == 'Добавить расход':
        await msg.reply('Какую сумму вы потратили?')
    elif text == 'Добавить доход':
        await msg.reply('Какую сумму вы получили?')
    elif text == 'Статистика':
        await msg.reply('За какой период вы хотите получить статистику?')
    else:
        await msg.reply('Извините, я вас не понял. Пожалуйста, воспользуйтесь клавиатурой с командами')


if __name__ == '__main__':
    executor.start_polling(dp)
