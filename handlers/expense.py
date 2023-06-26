from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from buttons import *


class ExpenseForm(StatesGroup):
    amount = State()
    reason = State()
    confirm = State()


async def add_expense(msg: types.Message):
    await msg.reply('Введите сумму расходов')
    await ExpenseForm.amount.set()


async def process_expense_amount(msg: types.Message, state: FSMContext):
    # TODO: ПРОВЕРКА НА ЧИСЛО
    text = msg.text
    await state.update_data(amount=text)
    await msg.answer('Теперь внесите причину расхода')
    await ExpenseForm.reason.set()


async def process_expense_reason(msg: types.Message, state: FSMContext):
    text = msg.text
    await state.update_data(reason=text)
    await msg.reply('Подтвердить внесение?', reply_markup=confirm_kb)
    await ExpenseForm.confirm.set()


async def process_expense_confirm_btn(callback_query: types.CallbackQuery, state: FSMContext):
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


def register_expense_handlers(dp: Dispatcher):
    dp.register_message_handler(add_expense, Text('Добавить расход'))
    dp.register_message_handler(process_expense_amount, state=ExpenseForm.amount)
    dp.register_message_handler(process_expense_reason, state=ExpenseForm.reason)
    dp.register_callback_query_handler(process_expense_confirm_btn, state=ExpenseForm.confirm)
