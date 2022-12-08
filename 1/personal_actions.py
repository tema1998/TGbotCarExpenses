from aiogram import types, Dispatcher
from Dispatcher import dp
import config
import re
from bot import BotDB

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Ни гвоздя, ни жезла :)")

@dp.message_handler(commands = ("Ремонт", "ремонт", "Топливо", "топливо"), commands_prefix = "/!")
async def record(message:types.Message):
    cmd_variants = (('/Ремонт', '/ремонт', '!Ремонт', '!ремонт'), ('/Топливо', '/топливо', '!Топливо', '!топливо'))
    repair_value = 0
    fuel_value = 0

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if (len(value)):
        x = re.findall(r"\d+(?:.\d+)?", value)

        if (len(x)):
            value = float(x[0].replace(',', '.'))

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

        else:
            await message.reply(f'Не удалось опеределить сумму!')

    else:
        await message.reply(f'Не введена сумма!')

@dp.message_handler(commands = ("История", "история"), commands_prefix = "/!")
async def record(message:types.Message):
    cmd_variants = ('/История', '/история', '!История', '!история')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "all": ('всё время'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '')

    within = 'day' #default
    if (len(cmd)):
        for k in within_als:
            for als in within_als[k]:
                if(als == cmd):
                    within = k

    records = BotDB.get_records(message.from_user.id, within)

    if(len(records)):
        answer = f"История операций за {within_als[within][-1]}\n\n"
        for r in records:
            answer += f"{r[3]}\n\n"
            answer += f"{r[4]}\n\n"
        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")



