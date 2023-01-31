import requests
from io import BytesIO
from aiogram import types
from loader import db, dp
from keyboards.default.menu import cats_markup, product_markup, make_amount_markup
from states.shop import AllStates
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=AllStates.product)
async def get_product(message: types.Message, state: FSMContext):
    product_title = message.text
    product = db.select_product(title=product_title)
    markup = make_amount_markup()
    text = f"<b>{product[1]} - {product[-3]} so'm</b>\n\n{product[2]}"
    await  state.update_data({"product_id": product[0], "text": text, "price": product[-3], "image": product[-2], "title": product[1]})
    text += f"\n\n<i><b>{product[1]} ({product[-3]}) x 1 = {product[-3]} so'm</b></i>"
    await message.answer_photo(photo=product[-2], caption=text, reply_markup=markup)
    await AllStates.next()

@dp.callback_query_handler(state=AllStates.amount)
async def get_amount(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    image = data.get("image")
    price = data.get("price")
    text = data.get("text")
    title = data.get("title")
    action, number = call.data.split("_")
    number = int(number)
    markup = make_amount_markup()
    if action == "add":
        markup = make_amount_markup(number=number + 1)
        text += f"\n\n<i><b>{title} ({price}) x {number + 1} = {(number + 1) * price} so'm</b></i>"
    elif action == "remove" and number > 1:
        markup = make_amount_markup(number=number - 1)
        text += f"\n\n<i><b>{title} ({price}) x {number - 1} = {(number - 1) * price} so'm</b></i>"
    response = requests.get(image)
    bytesio = BytesIO(response.content)
    media_photo = types.InputMediaPhoto(media=types.InputFile(path_or_bytesio=bytesio), caption=text)
    if action == "remove" and number > 1:
        await call.message.edit_media(media=media_photo, reply_markup=markup)
    elif action == "add":
        await call.message.edit_media(media=media_photo, reply_markup=markup)
    else:
        pass