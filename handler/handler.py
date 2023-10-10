from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message)
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from config.settings_db import connection

router = Router()

cursor = connection.cursor()

# --- id_photo ---
@router.message(F.photo)
async def message_handler(msg: Message):
    id_photo = msg.photo[0].file_id
    await msg.answer(str(id_photo))

# --- /start ---
@router.message(Command("start"))
async def start_menu(msg: Message):
    cursor.execute("UPDATE choose SET bolshoe='0', malenkoe='0', studia='0', temnoe= '0', svetloe='0', pryamoyg='0', kvadrat = '0'")
    cursor.execute("UPDATE target_kitchen SET gotovit='0', vstr='0', work='0'")
    cursor.execute("UPDATE emotions SET calm='0', joy='0', bright='0'")
    cursor.execute("UPDATE frequency SET everday='0', cherday='0', threeday='0',weekday='0'")
    cursor.execute("UPDATE dishes SET yes='0', no='0'")
    cursor.execute("UPDATE family_member SET one='0', two='0', threemore='0'")
    cursor.execute("UPDATE children SET yes1='0', no1='0'")
    cursor.execute("UPDATE wishes SET wish='0'")
    cursor.execute("UPDATE message_personal SET name='0', number='0', email='0'")
    connection.commit()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [[
            InlineKeyboardButton(text = "Подобрать кухню", callback_data="choose")
        ]]
    )
    await msg.answer_photo("AgACAgIAAxkBAAIFq2UjyOql9jWvST9rNGndnyMqnU53AAITzzEby6ohST0EeMAiy8cyAQADAgADcwADMAQ",
                           f"Добрый день, {msg.from_user.username}, не знаете, какая кухня Вам подходит?"
                           f"Ответьте на 8 вопросов и наш специалист подберет варианты кухонь под особенности помещения,"
                           f" количество членов семьи, частоты использования и пожеланий.", reply_markup=keyboard)

    await msg.delete()




