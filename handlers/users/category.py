from aiogram import types
from loader import db, dp
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import cats_markup, product_markup, main
from states.shop import AllStates

@dp.message_handler(text="⬅️ Orqaga", state=AllStates.category)
async def back_to_main(message: types.Message, state: FSMContext):
    await message.answer(text="Siz asosiy menyudasiz", reply_markup=main)
    await state.finish()

@dp.message_handler(state=AllStates.category)
async def get_cat_product(message: types.Message, state: FSMContext):
    cat_title = message.text
    cat_id = db.select_cat(title=cat_title)[0]
    await state.update_data({"cat_id": cat_id})
    products = db.select_products(cat_id=cat_id)
    markup = product_markup(products)
    if products:
        await message.answer("Quyidagi mahsulotlardan birini tanlang", reply_markup=markup)
        await AllStates.next()
    else:
        await message.answer("Hozircha bu kategoriyada mahsulot yo'q")

@dp.message_handler(state=AllStates.cart)
async def get_cat_product(message: types.Message, state: FSMContext):
    cat_title = message.text
    cat_id = db.select_cat(title=cat_title)[0]
    await state.update_data({"cat_id": cat_id})
    products = db.select_products(cat_id=cat_id)
    markup = product_markup(products)
    if products:
        await message.answer("Quyidagi mahsulotlardan birini tanlang", reply_markup=markup)
        await AllStates.product.set()
    else:
        await message.answer("Hozircha bu kategoriyada mahsulot yo'q")
