from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

def get_button_text(ikbs):
    return [i.callback_data for i in ikbs]

def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Add', callback_data = '/add'))
    kb.add(KeyboardButton('History', callback_data = '/history'))
    return kb


def get_cancel1() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('/cancel'))

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


choose_group = InlineKeyboardMarkup(row_width=2)
x0 = InlineKeyboardButton(text = 'Fuel', callback_data="fuel")
x1 = InlineKeyboardButton(text = 'Repair', callback_data="repair")
choose_group.add(x0, x1)

choose_groups = InlineKeyboardMarkup(row_width=2)
u0 = InlineKeyboardButton(text = 'Fuel', callback_data="fuel")
u1 = InlineKeyboardButton(text = 'Repair', callback_data="repair")
u3 = InlineKeyboardButton(text = 'All', callback_data="all")
choose_groups.add(u0, u1, u3)

choose_date = InlineKeyboardMarkup(row_width=1)
z0 = InlineKeyboardButton(text = 'Today', callback_data="today")
z1 = InlineKeyboardButton(text = 'Yesterday', callback_data="yesterday")
z2 = InlineKeyboardButton(text = 'Enter date', callback_data="enter_date")
choose_date.add(z0, z1, z2)



#Клавиатура для year
ikbyear = InlineKeyboardMarkup(row_width=1)
a0 = InlineKeyboardButton(text = 'All time', callback_data="all")
a1 = InlineKeyboardButton(text = '2020', callback_data="2020")
a2 = InlineKeyboardButton(text = '2021', callback_data="2021")
a3 = InlineKeyboardButton(text = '2022', callback_data="2022")
ikbyear.add(a0,a1,a2,a3)

#Клавиатура для months
ikbmonth = InlineKeyboardMarkup(row_width=3)
b1 = InlineKeyboardButton(text = 'January', callback_data="1")
b2 = InlineKeyboardButton(text = 'February', callback_data="2")
b3 = InlineKeyboardButton(text = 'March', callback_data="3")
b4 = InlineKeyboardButton(text = 'April', callback_data="4")
b5 = InlineKeyboardButton(text = 'May', callback_data="5")
b6 = InlineKeyboardButton(text = 'June', callback_data="6")
b7 = InlineKeyboardButton(text = 'July', callback_data="7")
b8 = InlineKeyboardButton(text = 'August', callback_data="8")
b9 = InlineKeyboardButton(text = 'September', callback_data="9")
b10 = InlineKeyboardButton(text = 'October', callback_data="10")
b11 = InlineKeyboardButton(text = 'November', callback_data="11")
b12 = InlineKeyboardButton(text = 'December', callback_data="12")
months=(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
ikbmonth.add(*months)
months=get_button_text(months)

#Клавиатура для year
reply_kb_detail = InlineKeyboardMarkup(row_width=1)
s1 = InlineKeyboardButton(text = 'Detail', callback_data="detail")
reply_kb_detail.add(s1)

