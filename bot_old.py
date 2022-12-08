import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Рандомное число')
    item2 = types.KeyboardButton('Как дела?')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.first_name}, меня зовут {bot.get_me().first_name}', parse_mode='html', reply_markup = markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    # bot.send_message(message.chat.id, message.text)
    # bot.send_message(message.chat.id, 'Скоро отвечу!')
    if message.chat.type == 'private':
        if message.text =='Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам(а) как?', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Даже не знаю что ответить')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает и такое. Всё будет хорошо!')

    except Exception as e:
        print(repr(e))
# RUN
bot.polling(none_stop=True)