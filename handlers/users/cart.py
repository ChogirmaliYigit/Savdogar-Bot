import requests
from io import BytesIO
from aiogram import types
from loader import db, dp
from keyboards.default.menu import cats_markup, product_markup, make_amount_markup, back_button_inline
from states.shop import AllStates
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text_contains="cart", state=AllStates.amount)
async def save_to_cart(call: types.CallbackQuery, state: FSMContext):
    quantity = call.data.split("_")[1]
    quantity = int(quantity)
    data = await state.get_data()
    product_id = data.get("product_id")

    product = db.select_cart_product(user_id=call.from_user.id, product_id=product_id)
    if product:
        quantity += product[-1]
        db.update_cart_product(user_id=call.from_user.id, product_id=product_id, quantity=quantity)
    else:
        db.add_product_to_cart(user_id=call.from_user.id, product_id=product_id, quantity=quantity)
    await call.answer("✅ Savatga qo'shildi")
    await call.message.delete()
    text = str()
    total_price = 0
    products = db.select_user_products(user_id=call.from_user.id)
    for product in products:
        mahsulot = db.select_product(id=product[2])
        price = mahsulot[-3] * quantity
        total_price += price
        text += f"<b>{mahsulot[1]}</b> x {quantity} = {price} so'm\n"
    text += f"\n✅ Savatga qo'shildi\n\nUmumiy narx: {total_price} so'm"
    await call.message.answer(text=text, reply_markup=cats_markup)
    await AllStates.category.set()


@dp.message_handler(text="🛒 Savat", state="*")
async def get_cart_products(message: types.Message):
    cart_markup = types.InlineKeyboardMarkup(row_width=1)
    text = str()
    total_price = 0
    products = db.select_user_products(user_id=message.from_user.id)
    for product in products:
        mahsulot = db.select_product(id=product[2])
        price = mahsulot[-3] * product[-1]
        total_price += price
        text += f"<b>{mahsulot[1]}</b> x {product[-1]} = {price} so'm\n"
        cart_markup.insert(types.InlineKeyboardButton(text=f"❌ {mahsulot[1]} ❌", callback_data=f"{product[1]}_{product[2]}"))
    text += f"\nUmumiy narx: {total_price} so'm"
    clear_cart = types.InlineKeyboardButton(text="🗑 Tozalash", callback_data="clear_cart")
    cart_markup.add(clear_cart, back_button_inline)
    await message.answer(text=text, reply_markup=cart_markup)
    await AllStates.cart.set()