import aiogram
import sqlite3
import logging
import asyncio
from aiogram import types
from loader import db, dp, bot
from keyboards.default.menu import phone_button, location_button, confirm, back_markup_inline, payment_markup
from states.shop import AllStates
from aiogram.dispatcher import FSMContext

@dp.callback_query_handler(text="order", state=AllStates.cart)
async def make_order(call: types.CallbackQuery, state: FSMContext):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
    inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
    await call.message.edit_text(text="Buyurtmani amalga oshirish uchun quyidagi ma'lumotlarni kiritishingiz so'raladi.", reply_markup=inline_markup)
    await state.update_data({"msg_id": call.message.message_id})
    await AllStates.order_note.set()

@dp.callback_query_handler(text="phone_number", state=AllStates.order_note)
async def send_phone_number_call(call: types.CallbackQuery):
    await call.message.answer(text="Raqamni jo'nating ⬇️", reply_markup=phone_button)
    await AllStates.get_phone.set()


@dp.message_handler(content_types=["contact"], state=AllStates.get_phone)
async def get_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("msg_id")
    address = data.get("address")
    phone = message.contact.phone_number
    await state.update_data({"phone": phone})
    label = True
    try:
        while label:
            if message.message_id > msg_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                message.message_id -= 1
            elif message.message_id == msg_id:
                inline_markup = types.InlineKeyboardMarkup(row_width=1)
                if phone:
                    inline_markup.add(types.InlineKeyboardButton(text="✅ Telefon raqam", callback_data="3"))
                    await AllStates.order_note.set()
                if not phone:
                    inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
                    await AllStates.order_note.set()
                if address:
                    inline_markup.add(types.InlineKeyboardButton(text="✅ Manzil", callback_data="4"))
                    await AllStates.order_note.set()
                if not address:
                    inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
                    await AllStates.order_note.set()
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=msg_id, reply_markup=inline_markup)
                if phone and address:
                    asyncio.sleep(1)
                    await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
                    await AllStates.order_confirm.set()
                label = False
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        inline_markup = types.InlineKeyboardMarkup(row_width=1)
        if phone:
            inline_markup.add(types.InlineKeyboardButton(text="✅ Telefon raqam", callback_data="3"))
            await AllStates.order_note.set()
        if not phone:
            inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
            await AllStates.order_note.set()
        if address:
            inline_markup.add(types.InlineKeyboardButton(text="✅ Manzil", callback_data="4"))
            await AllStates.order_note.set()
        if not address:
            inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
            await AllStates.order_note.set()
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=msg_id, reply_markup=inline_markup)
        if phone and address:
            asyncio.sleep(1)
            await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
            await AllStates.order_confirm.set()

@dp.callback_query_handler(text="address", state=AllStates.order_note)
async def send_address_call(call: types.CallbackQuery):
    await call.message.answer(text="Manzilni jo'nating ⬇️", reply_markup=location_button)
    await AllStates.get_address.set()


@dp.message_handler(content_types=["location"], state=AllStates.get_address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data({"address": message.location, "lat": message.location.latitude, "lon": message.location.longitude})
    data = await state.get_data()
    msg_id = data.get("msg_id")
    phone = data.get("phone")
    address = data.get("address")
    label = True
    try:
        while label:
            if msg_id < message.message_id:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                message.message_id -= 1
            elif msg_id == message.message_id:
                inline_markup = types.InlineKeyboardMarkup(row_width=1)
                if phone:
                    inline_markup.add(types.InlineKeyboardButton(text="✅ Telefon raqam", callback_data="3"))
                    await AllStates.order_note.set()
                if not phone:
                    inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
                    await AllStates.order_note.set()
                if address:
                    inline_markup.add(types.InlineKeyboardButton(text="✅ Manzil", callback_data="4"))
                    await AllStates.order_note.set()
                if not address:
                    inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
                    await AllStates.order_note.set()
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=msg_id, reply_markup=inline_markup)    
                if phone and address:
                    asyncio.sleep(1)
                    await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
                    await AllStates.order_confirm.set()
                label = False
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        inline_markup = types.InlineKeyboardMarkup(row_width=1)
        if phone:
            inline_markup.add(types.InlineKeyboardButton(text="✅ Telefon raqam", callback_data="3"))
            await AllStates.order_note.set()
        if not phone:
            inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
            await AllStates.order_note.set()
        if address:
            inline_markup.add(types.InlineKeyboardButton(text="✅ Manzil", callback_data="4"))
            await AllStates.order_note.set()
        if not address:
            inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
            await AllStates.order_note.set()
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=msg_id, reply_markup=inline_markup)    
        if phone and address:
            asyncio.sleep(1)
            await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
            await AllStates.order_confirm.set()


@dp.callback_query_handler(state=AllStates.order_confirm)
async def order_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    lat = data.get("lat")
    lon = data.get("lon")
    confirm = call.data.split("_")[-1]
    if confirm == "true":
        try:
            db.add_order_product(user_id=call.from_user.id, phone=f"+{phone}", lat=lat, lon=lon, paid="0")
        except sqlite3.Error as error:
            logging.error(error)
        products = db.select_user_products(user_id=call.from_user.id)
        text = str()
        total_price = 0
        for product in products:
            mahsulot = db.select_product(id=product[2])
            price = mahsulot[-3] * product[-1]
            total_price += price
            text += f"<b>{mahsulot[1]}</b> x {product[-1]} = {price} so'm\n"
        text += f"\nUmumiy narx: {total_price} so'm\nYetkazish manzili: {lat}, {lon}"
        await call.message.edit_text(text=text, reply_markup=payment_markup)
        await AllStates.paid_state.set()
        # await call.answer(text="✅ Buyurtmangiz qabul qilindi")
    elif confirm == "false":
        await call.answer("❌ Buyurtma bekor qilindi")
        products = db.select_user_products(user_id=call.from_user.id)
        order = types.InlineKeyboardButton(text="🚚 Buyurtma berish", callback_data="order")
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
        cart_markup.row(clear_cart, back_markup_inline)
        await call.message.answer(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    elif confirm == "retry":
        inline_markup = types.InlineKeyboardMarkup(row_width=1)
        inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
        inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
        await call.message.edit_text(text="Buyurtmani amalga oshirish uchun quyidagi ma'lumotlarni kiritishingiz so'raladi.", reply_markup=inline_markup)
        await AllStates.order_note.set()

@dp.callback_query_handler(text="back", state=AllStates.paid_state)
async def back_to_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    await call.message.edit_text(text=f"Telefon: <b>+{phone}</b>\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>")
    await AllStates.order_confirm.set()