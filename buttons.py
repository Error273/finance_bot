from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.add(KeyboardButton('Добавить расход'), KeyboardButton('Добавить доход'), KeyboardButton('Статистика'))

choose_statistics_period_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton('За неделю', callback_data='btn_week')).add(
    InlineKeyboardButton('За месяц', callback_data='btn_month')).add(
    InlineKeyboardButton('За все время', callback_data='btn_all_time'))

confirm_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Отмена', callback_data='btn_cancel')).add(
    InlineKeyboardButton('Да', callback_data='btn_confirm'))


def get_categories_kb(categories):
    print(categories)
    kb = InlineKeyboardMarkup()
    for i in categories:
        category = i[0]
        kb.add(InlineKeyboardButton(category, callback_data=f'btn_category_{category}'))
    return kb