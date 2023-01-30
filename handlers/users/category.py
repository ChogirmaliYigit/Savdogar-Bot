from aiogram import types
from loader import db, dp
from keyboards.default.menu import cats_markup, product_markup
from states.shop import AllStates

@dp.message_handler(state=AllStates.category)
async def get_cat_product(message: types.Message):
    cat_title = message.text
    cat_id = db.select_cat(title=cat_title)[0]
    products = db.select_products(cat_id=cat_id)
    markup = product_markup(products)
    if products:
        await message.answer("Quyidagi mahsulotlardan birini tanlang", reply_markup=markup)
        await AllStates.next()
    else:
        await message.answer("Hozircha bu kategoriyada mahsulot yo'q")