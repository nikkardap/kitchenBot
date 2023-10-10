from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message)
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

import psycopg2

from config.settings_db import connection

class FSMRegMessage(StatesGroup):
    message = State()

class FSMContactData(StatesGroup):
    name = State()
    number_phone = State()
    client_email = State()

router = Router()
list_of_subject = []

cursor = connection.cursor()
cursor.execute("SELECT * FROM choose")

#--- выбор характеристики помещения ---
@router.callback_query(lambda F: F.data == "choose" or F.data == "bolshoe" or F.data =="malenkoe" or F.data =="studia" or F.data =="temnoe" or F.data =="svetloe" or F.data =="pryamoyg" or F.data =="kvadrat")
async def new_choose_kitchen(callback: CallbackQuery):
    # --- список для выбора ---
    spis = ["bolshoe", "malenkoe", "studia", "temnoe", "svetloe", "pryamoyg", "kvadrat"]
    cursor.execute("SELECT * FROM choose")
    # --- цикл чтобы знать на какую кнопку нажимает пользователь и менять её состояние ---
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE choose SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM choose")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ большое" if fetch[0] == '0' else "✅ большое"),
                                 callback_data="bolshoe"),
            InlineKeyboardButton(text=("➖ маленькое" if fetch[1] == '0' else "✅ маленькое"), callback_data="malenkoe"),
            InlineKeyboardButton(text=("➖ студия" if fetch[2] == '0' else "✅ студия"), callback_data="studia")], [
            InlineKeyboardButton(text=("➖ темное" if fetch[3] == '0' else "✅ темное"), callback_data="temnoe")], [
            InlineKeyboardButton(text=("➖ светлое" if fetch[4] == '0' else "✅ светлое"), callback_data="svetloe"),
            InlineKeyboardButton(text=("➖ прямоугольное" if fetch[5] == '0' else "✅ прямоугольное"), callback_data="pryamoyg"),
            InlineKeyboardButton(text=("➖ квадратное" if fetch[6] == '0' else "✅ квадратное"), callback_data="kvadrat")], [
            InlineKeyboardButton(text="Далее", callback_data="dalee")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Выберите характеристики помещения", reply_markup=keyboard)

    await callback.message.delete()

#--- выбор цели кухонной гарнитуры ---
@router.callback_query(lambda F: F.data == "dalee" or F.data == "gotovit" or F.data == "vstr" or F.data == "work")
async def target(callback: CallbackQuery):
    spis = ["gotovit", "vstr", "work"]
    cursor.execute("SELECT * FROM target_kitchen")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE target_kitchen SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM target_kitchen")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ готовить" if fetch[0]=='0' else "✅ готовить"), callback_data="gotovit"),
            InlineKeyboardButton(text=("➖ встречать гостей" if fetch[1]=='0' else "✅ встречать гостей"), callback_data="vstr"),
            InlineKeyboardButton(text=("➖ использовать в том числе как рабочее место" if fetch[2]=='0' else "✅ использовать в том числе как рабочее место"),callback_data="work"),
            InlineKeyboardButton(text="Назад", callback_data="choose"),
            InlineKeyboardButton(text="Далее", callback_data="dalee1")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Выберите для каких целей требуется кухонный гарнитур", reply_markup=keyboard
    )
    await callback.message.delete()

#--- выбор какой должна быть кухня ---
@router.callback_query(lambda F: F.data == "dalee1" or F.data == "calm" or F.data == "joy" or F.data == "bright")
async def target(callback: CallbackQuery):
    spis = ["calm", "joy", "bright"]
    cursor.execute("SELECT * FROM emotions")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE emotions SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM emotions")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ спокойной" if fetch[0]=='0' else "✅ спокойной"), callback_data="calm"),
            InlineKeyboardButton(text=("➖ радостной" if fetch[1]=='0' else "✅ радостной"), callback_data="joy"),
            InlineKeyboardButton(text=("➖ яркой" if fetch[2]=='0' else "✅ яркой"),callback_data="bright"),
            InlineKeyboardButton(text="Назад", callback_data="dalee"),
            InlineKeyboardButton(text="Далее", callback_data="dalee2")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Какой должна быть кухня?", reply_markup=keyboard
    )
    await callback.message.delete()

#--- выбор частоты готовки ---
@router.callback_query(lambda F: F.data == "dalee2" or F.data == "everday" or F.data == "cherday" or F.data == "threeday" or F.data == "weekday")
async def target(callback: CallbackQuery):
    spis = ["everday", "cherday", "threeday", "weekday"]
    cursor.execute("SELECT * FROM frequency")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE frequency SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM frequency")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ каждый день" if fetch[0]=='0' else "✅ каждый день"), callback_data="everday"),
            InlineKeyboardButton(text=("➖ через день" if fetch[1]=='0' else "✅ через день"), callback_data="cherday"),
            InlineKeyboardButton(text=("➖ раз в три дня" if fetch[2]=='0' else "✅ раз в три дня"),callback_data="threeday"),
            InlineKeyboardButton(text=("➖ раз в неделю" if fetch[3] == '0' else "✅ раз в неделю"),
                                 callback_data="weekday"),
            InlineKeyboardButton(text="Назад", callback_data="dalee1"),
            InlineKeyboardButton(text="Далее", callback_data="dalee3")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Как часто вы будете готовить?", reply_markup=keyboard
    )
    await callback.message.delete()

#--- сколько посуды для хранения ---
@router.callback_query(lambda F: F.data == "dalee3" or F.data == "yes" or F.data == "no")
async def target(callback: CallbackQuery):
    spis = ["yes", "no"]
    cursor.execute("SELECT * FROM dishes")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE dishes SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM dishes")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ да" if fetch[0]=='0' else "✅ да"), callback_data="yes"),
            InlineKeyboardButton(text=("➖ нет" if fetch[1]=='0' else "✅ нет"), callback_data="no"),
            InlineKeyboardButton(text="Назад", callback_data="dalee2"),
            InlineKeyboardButton(text="Далее", callback_data="dalee4")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "У вас много посуды для хранения?", reply_markup=keyboard
    )
    await callback.message.delete()


#--- сколько членов семьи используют кухню ---
@router.callback_query(lambda F: F.data == "dalee4" or F.data == "one" or F.data == "two" or F.data == "threemore")
async def target(callback: CallbackQuery):
    spis = ["one", "two", "threemore"]
    cursor.execute("SELECT * FROM family_member")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE family_member SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM family_member")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ один" if fetch[0]=='0' else "✅ один"), callback_data="one"),
            InlineKeyboardButton(text=("➖ два" if fetch[1]=='0' else "✅ два"), callback_data="two"),
            InlineKeyboardButton(text=("➖ три и более" if fetch[2]=='0' else "✅ три и более"),callback_data="threemore"),
            InlineKeyboardButton(text="Назад", callback_data="dalee3"),
            InlineKeyboardButton(text="Далее", callback_data="dalee5")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Сколько членов семьи будут пользоваться кухней?", reply_markup=keyboard
    )
    await callback.message.delete()


#--- маленькие дети ---
@router.callback_query(lambda F: F.data == "dalee5" or F.data == "yes1" or F.data == "no1")
async def target(callback: CallbackQuery):
    spis = ["yes1", "no1"]
    cursor.execute("SELECT * FROM children")
    for i in range(len(spis)):
        if str(callback.data) == spis[i]:
            cursor.execute("UPDATE children SET " + str(callback.data) + "=" + str(1 if cursor.fetchone()[i] == '0' else 0))
            connection.commit()
    cursor.execute("SELECT * FROM children")
    fetch = cursor.fetchone()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=("➖ да" if fetch[0]=='0' else "✅ да"), callback_data="yes1"),
            InlineKeyboardButton(text=("➖ нет" if fetch[1]=='0' else "✅ нет"), callback_data="no1"),
            InlineKeyboardButton(text="Назад", callback_data="dalee4"),
            InlineKeyboardButton(text="Далее", callback_data="dalee6")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Есть ли маленькие дети?", reply_markup=keyboard
    )
    await callback.message.delete()


#--- пожелания к кухне ---
@router.callback_query(lambda F: F.data == "dalee6")
async def target(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Назад", callback_data="dalee5"),
            InlineKeyboardButton(text="Далее", callback_data="dalee7")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Опишите в свободной форме свои пожелания к кухне", reply_markup=keyboard
    )
    await state.set_state(FSMRegMessage.message)
    await callback.message.delete()

#--- сохранение пожелании ---
@router.message(FSMRegMessage.message, F.text)
async def set_message(msg: Message, state: FSMContext):
    await state.update_data(message = msg.text)
    await state.set_state(FSMRegMessage.message.state)
    data = await state.update_data()
    print(data['message'])
    cursor.execute("UPDATE wishes SET wish = '"+str(data['message'])+"';")
    connection.commit()
    await state.clear()

#--- контактные данные ---
@router.callback_query(lambda F: F.data == "dalee7")
async def save_message(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text = "Ваше имя", callback_data="name_client"),
            InlineKeyboardButton(text = "Номер телефона", callback_data="number_phone"),
            InlineKeyboardButton(text = "Почта", callback_data="mail")
        ]]
    )
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Спасибо за ответы!\n Осталось ввести контактные данные: ", reply_markup=keyboard
    )
    await callback.message.delete()

#--- имя клиента ---
@router.callback_query(lambda F: F.data == "name_client")
async def save_message(callback: CallbackQuery, state: FSMContext):
    cursor.execute("SELECT * FROM message_personal;")
    fetch = cursor.fetchone()
    if fetch[0] == '0' and fetch[1] == '0' and fetch[2] == '0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text = "Номер телефона", callback_data="number_phone"),
                InlineKeyboardButton(text = "Почта", callback_data="mail")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Ваше имя: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.name)
    elif fetch[0]=='0' and fetch[1]!='0' and fetch[2]=='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Почта", callback_data="mail")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Ваше имя: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.name)
    elif fetch[0]=='0' and fetch[1]=='0' and fetch[2]!='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Номер телефона", callback_data="number_phone")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Ваше имя: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.name)
    elif fetch[0]=='0' and fetch[1]!='0' and fetch[2]!='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Отправить", callback_data="otpravka")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Введите ваше имя и нажмите кнопку отправить: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.name)
    await callback.message.delete()

#--- сохранение контактных данных имени ---
@router.message(FSMContactData.name, F.text)
async def contact_data(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)
    await state.set_state(FSMContactData.name.state)
    data = await state.update_data()
    cursor.execute("UPDATE message_personal SET name = '"+str(data['name'])+"';")
    connection.commit()
    await state.clear()

#--- номер телефона ---
@router.callback_query(lambda F: F.data == "number_phone")
async def save_message(callback: CallbackQuery, state: FSMContext):
    cursor.execute("SELECT * FROM message_personal;")
    fetch = cursor.fetchone()
    if fetch[0] == '0' and fetch[1] == '0' and fetch[2] == '0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text = "Ваше имя", callback_data="name_client"),
                InlineKeyboardButton(text = "Почта", callback_data="mail")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Номер телефона: ", reply_markup=keyboard
    )
        await state.set_state(FSMContactData.number_phone)
    elif fetch[0]!='0' and fetch[1]=='0' and fetch[2]=='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Почта", callback_data="mail")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Номер телефона: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.number_phone)
    elif fetch[0]=='0' and fetch[1]=='0' and fetch[2]!='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Ваше имя", callback_data="name_client")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Номер телефона: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.number_phone)
    elif fetch[0]!='0' and fetch[1]=='0' and fetch[2]!='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Отправить", callback_data="otpravka")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Введите номер телефона и нажмите кнопку отправить: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.number_phone)
    await callback.message.delete()

#--- сохранение контактных данных номера телефона ---
@router.message(FSMContactData.number_phone, F.text)
async def contact_data(msg: Message, state: FSMContext):
    await state.update_data(number_phone = msg.text)
    await state.set_state(FSMContactData.number_phone.state)
    data = await state.update_data()
    cursor.execute("UPDATE message_personal SET number = '"+str(data['number_phone'])+"';")
    connection.commit()
    await state.clear()

#--- почта ---
@router.callback_query(lambda F: F.data == "mail")
async def save_message(callback: CallbackQuery, state: FSMContext):
    cursor.execute("SELECT * FROM message_personal;")
    fetch = cursor.fetchone()
    if fetch[0] == '0' and fetch[1] == '0' and fetch[2] == '0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text = "Ваше имя", callback_data="name_client"),
                InlineKeyboardButton(text = "Номер телефона", callback_data="number_phone")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Почта: ", reply_markup=keyboard
    )
        await state.set_state(FSMContactData.client_email)
    elif fetch[0]!='0' and fetch[1]=='0' and fetch[2]=='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Номер телефона", callback_data="number_phone")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Почта: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.client_email)
    elif fetch[0]=='0' and fetch[1]!='0' and fetch[2]=='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Ваше имя", callback_data="name_client")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Почта: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.client_email)
    elif fetch[0]!='0' and fetch[1]!='0' and fetch[2]=='0':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Отправить", callback_data="otpravka")
            ]]
        )
        await callback.message.answer_photo(
            "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
            "Введите почту и нажмите кнопку отправить: ", reply_markup=keyboard
        )
        await state.set_state(FSMContactData.client_email)
    await callback.message.delete()

#--- сохранение контактных данных номера телефона ---
@router.message(FSMContactData.client_email, F.text)
async def contact_data(msg: Message, state: FSMContext):
    await state.update_data(client_email = msg.text)
    await state.set_state(FSMContactData.client_email.state)
    data = await state.update_data()
    cursor.execute("UPDATE message_personal SET email = '"+str(data['client_email'])+"';")
    connection.commit()
    await state.clear()

#--- Отправка специалисту---
@router.callback_query(F.data == "otpravka")
async def otpr_spec(callback: CallbackQuery):
    cursor.execute("SELECT * FROM message_personal;")
    fetch = cursor.fetchone()
    print(fetch[0],"\n",fetch[1],"\n",fetch[2])
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
        "Специалист проанализирует информацию и предложит лучшее решение по планировке, цветам, компоновке и фукнциональной части исходя из Ваших пожеланий."
    )
    await callback.message.delete()