from aiogram import types
from loader import db, dp
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import cats_markup, make_back_button
from states.shop import AllStates

@dp.message_handler(text="🛍 Xarid qilish")
async def main_menu(message: types.Message):
    await message.answer(text="Bizning barcha kategoriyalar shulardan iborat. Nima xarid qilishni xohlaysiz?", reply_markup=cats_markup)
    await AllStates.category.set()

@dp.message_handler(text="🛒 Savat")
async def cart_main(message: types.Message, state: FSMContext):
    products = db.select_user_products(user_id=message.from_user.id)
    order_button = types.InlineKeyboardButton(text="🚚 Buyurtma berish", callback_data="order")
    if products:
        cart_markup = types.InlineKeyboardMarkup(row_width=1)
        cart_markup.add(order_button)
        text = str()
        total_price = 0
        for product in products:
            mahsulot = db.select_product(id=product[2])
            price = mahsulot[-3] * product[-1]
            total_price += price
            text += f"<b>{mahsulot[1]}</b> x {product[-1]} = {price} so'm\n"
            cart_markup.insert(types.InlineKeyboardButton(text=f"❌ {mahsulot[1]} ❌", callback_data=f"{product[1]}_{product[2]}"))
        text += f"\nUmumiy narx: {total_price} so'm"
        clear_cart = types.InlineKeyboardButton(text="🗑 Tozalash", callback_data="clear_cart")
        cart_markup.row(clear_cart, make_back_button(call_data="main"))
        await state.update_data({"call_data": "product"})
        await message.answer(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    else:
        await message.answer(text="Savatingiz bo'sh. Nimadir xarid qiling")