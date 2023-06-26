from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from buttons import *


class IncomeForm(StatesGroup):
    amount = State()
    reason = State()
    confirm = State()


async def add_income(msg: types.Message):
    await msg.reply('Введите сумму дохода')
    await IncomeForm.amount.set()


async def process_income_amount(msg: types.Message, state: FSMContext):
    # TODO: ПРОВЕРКА НА ЧИСЛО
    text = msg.text
    await state.update_data(amount=text)
    await msg.answer('Теперь внесите причину дохода')
    await IncomeForm.reason.set()


async def process_income_reason(msg: types.Message, state: FSMContext):
    text = msg.text
    await state.update_data(reason=text)
    await msg.reply('Подтвердить внесение?', reply_markup=confirm_kb)
    await IncomeForm.confirm.set()


async def process_income_confirm_btn(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    if code == 'btn_confirm':
        data = await state.get_data()
        await callback_query.answer(str(data))
        await callback_query.message.delete_reply_markup()
        await state.finish()

    elif code == 'btn_cancel':
        await state.reset_state()
        await callback_query.answer('Отменено!')
        await callback_query.message.delete_reply_markup()
        await state.finish()


def register_income_handlers(dp: Dispatcher):
    dp.register_message_handler(add_income, Text('Добавить доход'))
    dp.register_message_handler(process_income_amount, state=IncomeForm.amount)
    dp.register_message_handler(process_income_reason, state=IncomeForm.reason)
    dp.register_callback_query_handler(process_income_confirm_btn, state=IncomeForm.confirm)
