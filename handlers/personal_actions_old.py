from aiogram import types
from datetime import datetime
from dispatcher import dp
import config
import re
from bot import BotDB
from keyboard import ikbyear, ikbmonth, reply_kb_detail
from keyboard import months, years
from aiogram.utils.markdown import hlink

HELP_COMMAND = """
<b>/help</b> - <em> список команд </em>
<b>/start</b> - <em> старт бота </em>
<b>/fuel сумма</b> - <em> расходы на топливо </em>
<b>/repair сумма</b> - <em> расходы на ремонт </em>
<b>/history </b> - <em> статистика </em>"""

@dp.message_handler(commands = ["help"])
async def help_command(message: types.Message):
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=HELP_COMMAND,
                                   parse_mode="HTML")


@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
    await message.bot.send_message(message.from_user.id, "Ни гвоздя, ни жезла :)")
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=HELP_COMMAND,
                                   parse_mode="HTML")


@dp.message_handler(commands = ("Ремонт", "ремонт", "Топливо", "топливо", "repair", "fuel"), commands_prefix = "/!")
async def record(message:types.Message):
    cmd_variants = (('/Ремонт', '/ремонт', '!Ремонт', '!ремонт', '!repair', '/repair'),
                    ('/Топливо', '/топливо', '!Топливо', '!топливо', '!fuel', '/fuel'))

    text = message.text
    text = text.split(' ')
    date_parsed = None
    if len(text) == 3:
        value = text[1]
        date = text[2]
        try:
            year = int(date.split('.')[2])
            if year < 2020 or year > 2022:
                raise ValueError('Неверный год!')
            date_parsed = datetime.strptime(date, "%d.%m.%Y")
        except Exception as ex:
            await message.reply(f'{ex}')
            return
    elif len(text) == 2:
        value = text[1]
    else:
        await message.reply(f'Введены некорректные данные! Примеры:')
        await message.reply(f'/fuel 50.5')
        await message.reply(f'/repair 50.5 01.01.2022')
        return

    try:
        value = float(value)
        if value > 9999999:
            raise Exception('Невозможно потратить данную сумму!')
    except ValueError as ex:
        await message.reply(f'{ex}')
    except Exception:
        await message.reply(f'Что-то введено неверно!')
        return

    if message.text.startswith(cmd_variants[0]):
        repair_value = value
        fuel_value = 0
        BotDB.add_record(message.from_user.id, repair_value, fuel_value)
        await message.reply(f'Добавлена запись: ремонт - {repair_value}')

    elif message.text.startswith(cmd_variants[1]):
        repair_value = 0
        fuel_value = value
        BotDB.add_record(message.from_user.id, repair_value, fuel_value)
        await message.reply(f'Добавлена запись: топливо - {fuel_value}')


@dp.message_handler(commands = ("history"), commands_prefix = "/!")
async def get_something(message:types.Message):
    await message.bot.send_message(chat_id=message.from_user.id,
                                    text='Выберите год',
                                    reply_markup=ikbyear)


glob_data= {}
@dp.callback_query_handler(text=years)
async def history_callback(callback: types.CallbackQuery):
    global glob_data
    if callback.data[:4] == 'year':
        glob_data['year']=callback.data[4:]
        await callback.message.edit_text('Выберите месяц')
        await callback.message.edit_reply_markup(ikbmonth)
    else:
        all_records = BotDB.get_all_records(user_id=callback.message.chat.id)
        glob_data['all_records'] = all_records
        if (len(all_records)):
            fuel = 0
            repair = 0
            answer = f"Статистика за <b>всё время</b>:\n"
            for r in all_records:
                fuel += int(r[3])
                repair += int(r[2])
            answer += f"    На топливо было потрачено: <b><em>{fuel} р.</em></b>\n"
            answer += f"    На ремонт было потрачено: <b><em>{repair} р.</em></b>\n"
            await callback.message.bot.send_message(chat_id=callback.message.chat.id, text=answer, reply_markup=reply_kb_detail)
            await callback.message.delete()


@dp.callback_query_handler(text=months)
async def history_callback(callback: types.CallbackQuery):
    global glob_data
    glob_data['month_number']=callback.data
    await get_records(message = callback.message, year = glob_data['year'],month=glob_data['month_number'])
    await callback.message.delete()


@dp.message_handler(commands = ("his"), commands_prefix = "/!")
async def get_records(message:types.Message, year, month):
    global glob_data
    records = BotDB.get_records(user_id=message.chat.id, year = glob_data['year'], month=glob_data['month_number'])
    glob_data['records']=records
    months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    glob_data['month_text'] = months[int(month)-1]
    if(len(records)):
        fuel = 0
        repair = 0
        answer = f"Статистика за <b>{glob_data['month_text']} {year}</b>:\n"
        for r in records:
            fuel += int(r[3])
            repair += int(r[2])
        answer += f"    На топливо было потрачено: <b><em>{fuel} р.</em></b>\n"
        answer += f"    На ремонт было потрачено: <b><em>{repair} р.</em></b>\n"
        await message.bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=reply_kb_detail)
    else:
        await message.bot.send_message(chat_id=message.chat.id, text=f"За <b>{glob_data['month_text']} {year}</b> затрат не было!")


@dp.callback_query_handler(text=['fuel_detail', 'repair_detail'])
async def detail(callback: types.CallbackQuery):
    if callback.message.text[14:17] == 'всё':
        date_year = f"всё время"
        records = glob_data['all_records']
    else:
        date_year = f"{glob_data['month_text']} {glob_data['year']}"
        records = glob_data['records']

    if callback.data[:4] == 'fuel':
        detail = f"Расходы на топливо за <b>{date_year}</b>: \n"
        month = 0
        for r in records:
            if r[3]!=0:
                if r[4][5:7] != month:
                    detail+=('\n')
                detail+=(f"<b><em>{str(r[3])} р.</em></b> - {r[4][8:10]}.{r[4][5:7]}.{r[4][:4]} - (id = {r[0]})\n")
                month = r[4][5:7]
        detail += (f"\n<b>/delete id</b> - для удаления записи.")
        await callback.message.answer(detail, parse_mode='HTML')
    else:
        detail = f"Расходы на ремонт за <b>{date_year}</b>: \n"
        for r in records:
            if r[2]!=0:
                detail+=(f"<b><em>{str(r[2])} р.</em></b> - {r[4][8:10]}.{r[4][5:7]}.{r[4][:4]} - (id = {r[0]})\n")
        detail += (f"\n<b>/delete id</b> - для удаления записи.")
        await callback.message.answer(detail)


@dp.message_handler(commands = ("delete"), commands_prefix = "/")
async def delete_record(message:types.Message):
    value = message.text
    value = value.replace('/delete', '').strip()

    try:
        if value:
            int(value)
            records = BotDB.delete_record(user_id=message.chat.id, record_id=value)
            await  message.answer(records)
        else:
            await  message.answer(f"Необходимо ввести <b>id</b>, например: <b>/delete 1</b>")

    except Exception:
        await  message.answer('<b>Id</b> может быть только целым числом!')



