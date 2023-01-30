from aiogram import types
from loader import db, dp
from keyboards.default.menu import cats_markup
from states.shop import AllStates

@dp.message_handler(text="🛍 Buyurtma berish")
async def main_menu(message: types.Message):
    await message.answer(text="Bizning barcha kategoriyalar shulardan iborat. Nima xarid qilishni xohlaysiz?", reply_markup=cats_markup)
    await AllStates.category.set()

