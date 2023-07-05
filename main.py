from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from buttons import *

from handlers import expense, income

from db import *
from excel import create_excel_file

from config import *

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

init_db('database.db')


async def statistics(msg: types.Message):
    await msg.reply('За какой период вы хотите получить статистику?', reply_markup=choose_statistics_period_kb)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_'))
async def process_callback_buttons(callback_query: types.CallbackQuery, state=FSMContext):
    code = callback_query.data
    if code == 'btn_week':
        data = get_db().get_data_week(callback_query.from_user.id)
        filename = create_excel_file(data, callback_query.from_user.id)
        await bot.send_document(callback_query.message.chat.id, open(filename, 'rb'))

    elif code == 'btn_month':
        data = get_db().get_data_month(callback_query.from_user.id)
        filename = create_excel_file(data, callback_query.from_user.id)
        await bot.send_document(callback_query.message.chat.id, open(filename, 'rb'))

    elif code == 'btn_all_time':
        data = get_db().get_data_all_time(callback_query.from_user.id)
        filename = create_excel_file(data, callback_query.from_user.id)
        await bot.send_document(callback_query.message.chat.id, open(filename, 'rb'))


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply(
        'Приветствую вас в боте для учета ваших финансов. Здесь вы можете контролировать ваши доходы и расходы!',
        reply_markup=main_kb)


expense.register_expense_handlers(dp)
income.register_income_handlers(dp)


@dp.message_handler()
async def main(msg: types.Message):
    text = msg.text
    if text == 'Добавить расход':
        await expense.add_expense(msg)
    elif text == 'Добавить доход':
        await income.add_income(msg)
    elif text == 'Статистика':
        await statistics(msg)
    else:
        await msg.reply('Извините, я вас не понял. Пожалуйста, воспользуйтесь клавиатурой с командами',
                        reply_markup=main_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
