import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import dp, db, bot
from states.shop import AdminStates
import pandas as pd

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/add_payment", user_id=ADMINS)
async def add_title_payment(message: types.Message):
    await message.answer(text="Payment title'ni kiriting")
    await AdminStates.add_title.set()

@dp.message_handler(state=AdminStates.add_title)
async def add_token_payment(message: types.Message, state: FSMContext):
    await state.update_data({"title": message.text})
    await message.answer(text="Payment token'ni kiriting")
    await AdminStates.add_token.set()

@dp.message_handler(state=AdminStates.add_token)
async def add_payment_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    try:
        db.add_payment_provider(title=title, token=message.text)
        await message.answer(text="Ma'lumotlar qo'shildi")
        await state.finish()
    except Exception as error:
        await message.answer(text="Ma'lumotlar qo'shilmadi")
        await state.finish()
        print(error)

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@BekoDev\n@chogirmali_blog\n\nkanallariga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")
