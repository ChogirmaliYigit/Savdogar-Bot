import aiogram
import sqlite3
import logging
import asyncio
from aiogram import types
from loader import db, dp, bot
from keyboards.default.menu import phone_button, location_button, confirm, make_back_button, payment_markup, main
from states.shop import AllStates
from aiogram.dispatcher import FSMContext
from geopy.geocoders import Nominatim
from utils.misc.payment import Product
from data.shipping import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from data.config import ADMINS


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
                    lat = data.get("lat")
                    lon = data.get("lon")
                    geolocator = Nominatim(user_agent="bot")
                    manzil = geolocator.geocode(str(lat) + "," + str(lon))
                    await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
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
            lat = data.get("lat")
            lon = data.get("lon")
            geolocator = Nominatim(user_agent="bot")
            manzil = geolocator.geocode(str(lat) + "," + str(lon))
            await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
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
                    lat = data.get("lat")
                    lon = data.get("lon")
                    geolocator = Nominatim(user_agent="bot")
                    manzil = geolocator.geocode(str(lat) + "," + str(lon))
                    await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
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
            data = await state.get_data()
            lat = data.get("lat")
            lon = data.get("lon")
            geolocator = Nominatim(user_agent="bot")
            manzil = geolocator.geocode(str(lat) + "," + str(lon))
            if phone.startswith("+"):
                await bot.edit_message_text(text=f"Telefon: <b>{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
            else:
                await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=message.chat.id, message_id=msg_id, reply_markup=confirm)
            await AllStates.order_confirm.set()


@dp.callback_query_handler(state=AllStates.order_confirm)
async def order_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    lat = data.get("lat")
    lon = data.get("lon")
    confirm = call.data.split("_")[-1]
    geolocator = Nominatim(user_agent="bot")
    manzil = geolocator.geocode(str(lat) + "," + str(lon))
    if confirm == "true":
        try:
            if phone.startswith("+"):
                db.add_order_product(user_id=call.from_user.id, phone=f"{phone}", address=str(manzil), lat=lat, lon=lon, paid="0")
            else:
                db.add_order_product(user_id=call.from_user.id, phone=f"+{phone}", address=str(manzil), lat=lat, lon=lon, paid="0")
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
        geolocator = Nominatim(user_agent="bot")
        manzil = geolocator.geocode(str(lat) + "," + str(lon))
        text += f"\nUmumiy narx: {total_price} so'm\nYetkazish manzili: <i>{manzil}</i>\n\nMarhamat, to'lovni amalga oshirishingiz mumkin.😊"
        payments = db.select_all_provider()
        await call.message.edit_text(text=text, reply_markup=payment_markup(payments))
        await AllStates.paid_state.set()
    elif confirm == "false":
        data = await state.get_data()
        address = data.get("address")
        phone = data.get("phone")
        if address and phone:
            await state.update_data({"address": None, "phone": None})
        await call.answer("❌ Buyurtma berish jarayoni bekor qilindi")
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
        cart_markup.row(clear_cart, make_back_button(call_data="order"))
        await call.message.answer(text=text, reply_markup=cart_markup)
        await AllStates.cart.set()
    # elif confirm == "retry":
    #     inline_markup = types.InlineKeyboardMarkup(row_width=1)
    #     inline_markup.add(types.InlineKeyboardButton(text="Telefon raqam", callback_data="phone_number"))
    #     inline_markup.add(types.InlineKeyboardButton(text="Manzil", callback_data="address"))
    #     await call.message.edit_text(text="Buyurtmani amalga oshirish uchun quyidagi ma'lumotlarni kiritishingiz so'raladi.", reply_markup=inline_markup)
    #     await AllStates.order_note.set()

@dp.callback_query_handler(text="back", state=AllStates.paid_state)
async def back_to_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("msg_id")
    phone = data.get("phone")
    lat = data.get("lat")
    lon = data.get("lon")
    geolocator = Nominatim(user_agent="bot")
    manzil = geolocator.geocode(str(lat) + "," + str(lon))
    if phone.startswith("+"):
        await bot.edit_message_text(text=f"Telefon: <b>{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=call.from_user.id, message_id=msg_id, reply_markup=confirm)
    else:
        await bot.edit_message_text(text=f"Telefon: <b>+{phone}</b>\nYetkazish manzili: {manzil}\n\n<i>Ma'lumotlaringizni tasdiqlaysizmi?</i>", chat_id=call.from_user.id, message_id=msg_id, reply_markup=confirm)
    await AllStates.order_confirm.set()

@dp.callback_query_handler(text="cancel", state=AllStates.paid_state)
async def cancel_payment_process(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="To'lov qilish bekor qilindi", reply_markup=main)
    await state.finish()

@dp.callback_query_handler(state=AllStates.paid_state)
async def get_payment(call: types.CallbackQuery):
    # await call.answer(text="To'lov provayderi hali ulanmagan😊", show_alert=True)
    provider = db.select_provider(title=call.data)
    products = db.select_user_products(user_id=call.from_user.id)
    text = str()
    prices = []
    for product in products:
        mahsulot = db.select_product(id=product[2])
        price = mahsulot[-3] * product[-1]
        prices.append(types.LabeledPrice(label=mahsulot[1], amount=int(price * 100)))
        text += f"{mahsulot[1]} x {product[-1]} = {price} so'm\n"
        order_product_id = db.select_order_products(user_id=call.from_user.id)[-1][0]
        db.add_order_item(product_id=mahsulot[0], quantity=product[-1], order_id=order_product_id)

    order = Product(
        title="To'lov qilish jarayoni",
        description=text,
        start_parameter="create_order_invoice",
        currency="UZS",
        prices=prices,
        provider_token=provider[-1],
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        is_flexible=True
    )
    await bot.send_invoice(chat_id=call.from_user.id, **order.generate_invoice(), payload=f"payload:{call.from_user.id}")

@dp.shipping_query_handler(state=AllStates.paid_state)
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "urganch":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)
    

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!", reply_markup=main)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}\nTel: {pre_checkout_query.order_info.phone_number}\nEmail: {pre_checkout_query.order_info.email}")
    try:
        order_product_id = db.select_order_products(user_id=pre_checkout_query.from_user.id)[-1][0]
        db.update_order_paid(paid=1, user_id=pre_checkout_query.from_user.id, id=order_product_id)
        db.clear_cart(user_id=pre_checkout_query.from_user.id)
    except Exception as error:
        print(error)
    await state.finish()

