import sqlite3
from aiogram import types
from loader import db, dp
from keyboards.default.menu import cats_markup, make_back_button, product_markup
from states.shop import AllStates
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="back_amount", state=AllStates.amount)
async def back_from_amount(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    cat_id = data.get("cat_id")
    products = db.select_products(cat_id=cat_id)
    markup = product_markup(products)
    await call.message.answer(text="Quyidagi mahsulotlardan birini tanlang", reply_markup=markup)
    await AllStates.product.set()

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
        price = mahsulot[-3] * product[-1]
        total_price += price
        text += f"<b>{mahsulot[1]}</b> x {product[-1]} = {price} so'm\n"
    text += f"\n✅ Savatga qo'shildi\n\nUmumiy narx: {total_price} so'm"
    await call.message.answer(text=text, reply_markup=cats_markup)
    await AllStates.category.set()


@dp.message_handler(text="🛒 Savat", state=AllStates.category)
async def get_cart_products(message: types.Message, state: FSMContext):
    products = db.select_user_products(user_id=message.from_user.id)
    order = types.InlineKeyboardButton(text="🚚 Buyurtma berish", callback_data="order")
    if products:
        cart_markup = types.InlineKeyboardMarkup(row_width=1)
        cart_markup.add(order)
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
        cart_markup.row(clear_cart, make_back_button(call_data="category"))
        await state.update_data({"call_data": "category"})
        await message.answer(text='Savatingiz 🛒', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    else:
        await message.answer(text="Savatingiz bo'sh. Nimadir xarid qiling")

@dp.message_handler(text="🛒 Savat", state=AllStates.product)
async def get_cart_products(message: types.Message, state: FSMContext):
    products = db.select_user_products(user_id=message.from_user.id)
    order = types.InlineKeyboardButton(text="🚚 Buyurtma berish", callback_data="order")
    if products:
        cart_markup = types.InlineKeyboardMarkup(row_width=1)
        cart_markup.add(order)
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
        cart_markup.row(clear_cart, make_back_button(call_data="product"))
        await state.update_data({"call_data": "product"})
        await message.answer(text='Savatingiz 🛒', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    else:
        await message.answer(text="Savatingiz bo'sh. Nimadir xarid qiling")

@dp.callback_query_handler(text="clear_cart", state=AllStates.cart)
async def clear_user_cart(call: types.CallbackQuery):
    db.clear_cart(user_id=int(call.from_user.id))
    await call.answer("Savatingiz bo'shatildi")
    await call.message.delete()
    await call.message.answer("Savatingiz bo'sh. Nimadir xarid qiling", reply_markup=cats_markup)
    await AllStates.category.set()

@dp.callback_query_handler(text_contains="back", state=AllStates.cart)
async def back_from_cart(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split("_")[-1]
    if call_data == "main":
        await call.message.delete()
        await call.message.answer(text="Siz asosiy menyudasiz")
        await state.finish()
    elif call_data == "category":
        await call.message.delete()
        await call.message.answer(text="Bizning barcha kategoriyalar shulardan iborat. Nima xarid qilishni xohlaysiz?")
        await AllStates.category.set()
    elif call_data == "product":
        await call.message.delete()
        data = await state.get_data()
        cat_id = data.get("cat_id")
        products = db.select_products(cat_id=cat_id)
        markup = product_markup(products)
        await call.message.answer(text="Quyidagi mahsulotlardan birini tanlang", reply_markup=markup)
        await AllStates.product.set()

@dp.callback_query_handler(state=AllStates.cart)
async def cart_detail(call: types.CallbackQuery, state: FSMContext):
    user_id, product_id = call.data.split("_")
    try:
        db.clear_cart(user_id=int(user_id), product_id=int(product_id))
    except sqlite3.OperationalError:
        await call.answer("Serverda muammo! Noqulaylik uchun uzr so'raymiz.", show_alert=True)
    order = types.InlineKeyboardButton(text="🚚 Buyurtma berish", callback_data="order")
    products = db.select_user_products(user_id=call.from_user.id)
    if products:
        cart_markup = types.InlineKeyboardMarkup(row_width=1)
        cart_markup.add(order)
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
        data = await state.get_data()
        call_data = data.get("call_data")
        cart_markup.row(clear_cart, make_back_button(call_data=call_data))
        await call.message.answer(text='Savatingiz 🛒', reply_markup=types.ReplyKeyboardRemove())
        await call.message.edit_text(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    else:
        await call.message.delete()
        await call.message.answer(text="Savatingiz bo'sh. Nimadir xarid qiling", reply_markup=cats_markup)
        await AllStates.category.set()
