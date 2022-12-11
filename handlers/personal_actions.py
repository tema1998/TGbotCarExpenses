from aiogram import types
from datetime import datetime, date
from dispatcher import dp
from bot import BotDB
from keyboard import ikbyear, ikbmonth, reply_kb_detail, choose_group, choose_date, choose_groups
from keyboard import get_keyboard, get_cancel

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


HELP_COMMAND = """
<b>/help</b> - <em> if you forget these commands. </em>
<b>/start</b> - <em> start work with bot. </em>
<b>/add</b> - <em> to add an expense </em>
<b>/history </b> - <em> history of your expenses </em>
You can use bot's keyboard instead of these commands.
Good luck!"""

@dp.message_handler(commands = ["help"])
async def help_command(message: types.Message):
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=HELP_COMMAND,
                                   parse_mode="HTML",
                                   reply_markup=get_keyboard())


@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=HELP_COMMAND,
                                   parse_mode="HTML",
                                   reply_markup=get_keyboard())


#FSM classes
class AddState(StatesGroup):
    RepairOrFuel = State()
    Expense = State()
    ExpenseDate = State()
    CheckDate = State()

class HistoryState(StatesGroup):
    RepairOrFuel = State()
    AllOrYear = State()
    Month = State()


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Successfully canceled!', reply_markup=get_keyboard())
    await state.finish()

#FSM add
#Start Add FSM
@dp.message_handler(Text(equals='Add', ignore_case=True), state=None)
@dp.message_handler(commands='add', commands_prefix = '!/', state=None)
async def start_work(message: types.Message) -> None:
    await AddState.RepairOrFuel.set()
    await message.delete()
    await message.answer(text='<em>Please, follow next instructions.</em>',
        reply_markup=get_cancel())
    await message.answer('<b>Choose an expense category:</b>',
                         reply_markup=choose_group)


@dp.message_handler(lambda message: message, state=AddState.RepairOrFuel)
async def check_group(message: types.Message):
    await message.reply('<em>Please, make a <b>choice</b> or /cancel !</em>')


@dp.callback_query_handler(text=['fuel', 'repair'] , state=AddState.RepairOrFuel)
async def save_group(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
         data['RepairOrFuel'] = callback.data
    await callback.message.delete()
    await callback.message.answer('Enter <b>amount</b>:')
    await AddState.next()


@dp.message_handler(lambda message: True if not message.text.isdigit() else True if int(message.text)>99999 else False , state=AddState.Expense)
async def check_expense(message: types.Message):
    await message.reply('<em>Please, enter correct <b>amount</b> or /cancel !</em>')


@dp.message_handler(state=AddState.Expense)
async def save_expense(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Expense'] = message.text
        data['user_id'] = message.from_user.id

    await AddState.next()
    await message.answer('Choose date:',
                         reply_markup=choose_date)


@dp.callback_query_handler(text=['today', 'yesterday', 'enter_date'] , state=AddState.ExpenseDate)
async def save_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data != 'enter_date':
        async with state.proxy() as data:
             data['ExpenseDate'] = callback.data


        async with state.proxy() as data:
            BotDB.add_record(data['RepairOrFuel'], data['user_id'], data['Expense'], data['ExpenseDate'])
            await callback.message.answer(
                f"Successful added <b>{data['Expense']}</b> rubles for <b>{data['RepairOrFuel']}ing</b> <b>{data['ExpenseDate']}!</b>",
                reply_markup=get_keyboard())

        await state.finish()
    else:
        await AddState.next()
        await callback.message.answer('Enter date, for example <b>01.01.2022</b>:')

def try_convert_data(date_text):
    try:
        date_converted = datetime.strptime(date_text, "%d.%m.%Y").date()
        if date_converted > date.today():
            return True
        return False
    except Exception:
        return True

@dp.message_handler(lambda message: try_convert_data(message.text) , state=AddState.CheckDate)
async def check_date(message: types.Message):
    await message.reply('<em>Please, enter correct date or /cancel !</em>')

@dp.message_handler(state=AddState.CheckDate)
async def enter_date_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ExpenseDate'] = datetime.strptime(message.text, "%d.%m.%Y").date()
        BotDB.add_record(data['RepairOrFuel'], data['user_id'], data['Expense'], data['ExpenseDate'])
        await message.answer(f"Successful added <b>{data['Expense']}</b> rubles for <b>{data['RepairOrFuel']}ing</b> <b>{data['ExpenseDate']}</b>!", reply_markup=get_keyboard())
        await message.delete()
    await state.finish()




#FSM history
@dp.message_handler(Text(equals='History', ignore_case=True), state=None)
@dp.message_handler(commands='history', commands_prefix = '!/', state=None)
async def start_finding_history(message: types.Message) -> None:
    await HistoryState.RepairOrFuel.set()
    await message.delete()
    await message.answer(text='<em>Please, follow next instructions.</em>',
        reply_markup=get_cancel())
    await message.answer('<b>Choose expenses category:</b>',
                         reply_markup=choose_groups)


@dp.message_handler(lambda message: message, state=HistoryState.RepairOrFuel)
async def check_groups(message: types.Message):
    await message.reply('<em>Please, make a <b>choice</b> or /cancel !</em>')


@dp.callback_query_handler(text=['fuel', 'repair', 'all'] , state=HistoryState.RepairOrFuel)
async def save_groups(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['RepairOrFuel'] = callback.data
        data['user_id'] = callback.message.chat.id
    await callback.message.delete()
    await callback.message.answer('Choose <b>year and month</b> or <b>all time</b>:', reply_markup= ikbyear)
    await HistoryState.next()


@dp.message_handler(lambda message: message, state=HistoryState.AllOrYear)
async def check_year(message: types.Message):
    await message.reply('<em>Please, make a <b>choice</b> or /cancel !</em>')

def get_fuel_answer(user_id, year=None, month=None):
    fuel = 0
    detail_fuel = f"<u><em>\nDetailing <b>fuel</b> expenses:</em> </u>\n"
    records = BotDB.get_all_fuel_records(user_id=user_id, year=year, month=month)
    for r in records:
        fuel += int(r[2])
        detail_fuel += (
            f"       <b><em>{str(r[2])} rubles</em></b> - {r[3][8:10]}.{r[3][5:7]}.{r[3][:4]} - ID: {str(r[0])} \n")
    answer = f"        Expenses for fueling: <b><em>{fuel} rubles.</em></b>\n"
    detail_fuel = None if fuel == 0 else detail_fuel
    return [answer, detail_fuel]

def get_repair_answer(user_id, year=None, month=None):
    repair = 0
    detail_repair = f"\n<u><em>Detailing <b>repair</b> expenses:</em> </u>\n"
    records = BotDB.get_all_repair_records(user_id=user_id, year=year, month=month)
    for r in records:
        repair += int(r[2])
        detail_repair += (
            f"       <b><em>{str(r[2])} rubles</em></b> - {r[3][8:10]}.{r[3][5:7]}.{r[3][:4]} - ID: {str(r[0])} \n")
    answer = f"        Expenses for repairing: <b><em>{repair} rubles.</em></b>\n"
    detail_repair = None if repair == 0 else detail_repair
    return [answer, detail_repair]

@dp.callback_query_handler(state=HistoryState.AllOrYear)
async def save_year(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'all':
        answer = f"History for <b>all time</b>:\n"

        async with state.proxy() as data:
            repair_or_fuel = data['RepairOrFuel']
            user_id = data['user_id']

        if repair_or_fuel == 'fuel':
            answ_and_detail = get_fuel_answer(user_id)
            answer = answer + answ_and_detail[0]
            if answ_and_detail[1] is not None:
                answer += answ_and_detail[1]
                # answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"
        elif repair_or_fuel == 'repair':
            answ_and_detail = get_repair_answer(user_id)
            answer = answer + answ_and_detail[0]
            if answ_and_detail[1] is not None:
                answer += answ_and_detail[1]
                # answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"
        else:
            f_answ_and_detail = get_fuel_answer(user_id)
            r_answ_and_detail = get_repair_answer(user_id)
            answer = answer + f_answ_and_detail[0] + r_answ_and_detail[0]
            if f_answ_and_detail[1] is not None:
                answer += f_answ_and_detail[1]
            if r_answ_and_detail[1] is not None:
                answer += r_answ_and_detail[1]
            # if r_answ_and_detail[1] is not None or f_answ_and_detail[1] is not None:
            #     answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"

        await callback.message.bot.send_message(chat_id=callback.message.chat.id, text=answer,
                                                reply_markup=get_keyboard(), disable_web_page_preview=True)
        await callback.message.delete()
        await state.finish()
    else:
        async with state.proxy() as data:
             data['year'] = callback.data
        await callback.message.delete()
        await callback.message.answer('Choose <b>month</b>:', reply_markup=ikbmonth)
        await HistoryState.next()


@dp.message_handler(lambda message: message, state=HistoryState.Month)
async def check_month(message: types.Message):
    await message.reply('<em>Please, make a <b>choice</b> or /cancel !</em>')


@dp.callback_query_handler(state=HistoryState.Month)
async def save_month(callback: types.CallbackQuery, state: FSMContext):
    fuel = 0
    repair = 0
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
              'December']
    async with state.proxy() as data:
        data['month'] = callback.data
        repair_or_fuel = data['RepairOrFuel']
        user_id = data['user_id']
        year = data['year']
        month = data['month']

    answer = f"<u>History for <b>{months[int(month)-1]} {year}</b>:</u>\n"

    if repair_or_fuel == 'fuel':
        answ_and_detail = get_fuel_answer(user_id, year, month)
        answer = answer + answ_and_detail[0]
        if answ_and_detail[1] is not None:
            answer += answ_and_detail[1]
            # answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"

    elif repair_or_fuel == 'repair':
        answ_and_detail = get_repair_answer(user_id, year, month)
        answer = answer + answ_and_detail[0]
        if answ_and_detail[1] is not None:
            answer += answ_and_detail[1]
            # answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"

    else:
        f_answ_and_detail = get_fuel_answer(user_id, year, month)
        r_answ_and_detail = get_repair_answer(user_id, year, month)
        answer = answer + f_answ_and_detail[0] + r_answ_and_detail[0]
        if f_answ_and_detail[1] is not None:
            answer += f_answ_and_detail[1]
        if r_answ_and_detail[1] is not None:
            answer += r_answ_and_detail[1]
        # if f_answ_and_detail[1] is not None or r_answ_and_detail[1] is not None:
        #     answer += f"<em>To delete an expense, use <b>/delete id</b></em>\n"

    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text=answer, reply_markup=get_keyboard())
    await callback.message.delete()
    await state.finish()


# @dp.message_handler(commands = ("delete"), commands_prefix = "/")
# async def delete_record(message:types.Message):
#     value = message.text
#     value = value.replace('/delete', '').strip()
#
#     try:
#         if value:
#             int(value)
#             records = BotDB.delete_record(user_id=message.chat.id, record_id=value)
#             await  message.answer(records)
#         else:
#             await  message.answer(f"You must enter an ID <b>id</b>, for example: <b>/delete 1</b>")
#
#     except Exception:
#         await  message.answer('<b>ID</b> can only be an integer!')
#


