from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

def get_button_text(ikbs):
    return [i.callback_data for i in ikbs]


#Клавиатура для year
ikbyear = InlineKeyboardMarkup(row_width=1)
a0 = InlineKeyboardButton(text = 'За всё время', callback_data="all")
a1 = InlineKeyboardButton(text = '2020', callback_data="year2020")
a2 = InlineKeyboardButton(text = '2021', callback_data="year2021")
a3 = InlineKeyboardButton(text = '2022', callback_data="year2022")
years=(a0,a1,a2,a3)
ikbyear.add(*years)
years=get_button_text(years)

#Клавиатура для months
ikbmonth = InlineKeyboardMarkup(row_width=3)
b1 = InlineKeyboardButton(text = 'Январь', callback_data="1")
b2 = InlineKeyboardButton(text = 'Февраль', callback_data="2")
b3 = InlineKeyboardButton(text = 'Март', callback_data="3")
b4 = InlineKeyboardButton(text = 'Апрель', callback_data="4")
b5 = InlineKeyboardButton(text = 'Май', callback_data="5")
b6 = InlineKeyboardButton(text = 'Июнь', callback_data="6")
b7 = InlineKeyboardButton(text = 'Июль', callback_data="7")
b8 = InlineKeyboardButton(text = 'Август', callback_data="8")
b9 = InlineKeyboardButton(text = 'Сентябрь', callback_data="9")
b10 = InlineKeyboardButton(text = 'Октябрь', callback_data="10")
b11 = InlineKeyboardButton(text = 'Ноябрь', callback_data="11")
b12 = InlineKeyboardButton(text = 'Декабрь', callback_data="12")
months=(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
ikbmonth.add(*months)
months=get_button_text(months)

#Клавиатура для year
reply_kb_detail = InlineKeyboardMarkup(row_width=2)
s1 = InlineKeyboardButton(text = 'ТОПЛИВО', callback_data="fuel_detail")
s2 = InlineKeyboardButton(text = 'РЕМОНТ', callback_data="repair_detail")
reply_kb_detail.add(s1, s2)