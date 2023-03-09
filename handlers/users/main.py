from aiogram import types
from loader import db, dp
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import cats_markup, make_back_button
from states.shop import AllStates

@dp.message_handler(text="🛍 Xarid qilish", state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Bizning barcha kategoriyalar shulardan iborat. Nima xarid qilishni xohlaysiz?", reply_markup=cats_markup)
    await AllStates.category.set()

@dp.message_handler(text="🛒 Savat", state='*')
async def cart_main(message: types.Message, state: FSMContext):
    await state.finish()
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


@dp.message_handler(text="📋 Buyurtmalarim", state='*')
async def get_user_orders(message: types.Message, state: FSMContext):
    await state.finish()
    # user_products = db.select_order_products(user_id=message.from_user.id)
    # if user_products:
    #     for product in user_products:
    #         user_order_item = db.select_order_item(order_id=product[0])
    #         product_id = user_order_item[1]
    #         quantity = user_order_item[1]
    #         products = db.select_product(id=product_id)
    #         await message.answer(text=f"#️⃣ Buyurtma raqami: {product[0]}\n*️⃣ Mahsulot nomi: {products[1]}\n🔢 Mahsulot miqdori: {quantity}\n📱 Telefon: {product[2]}\n📍 Yetkaziladigan manzil: {product[3]}")
    # else:
    await message.answer(text="<i>Bot test rejimida ishlayotgani sababli buyurtmalar qabul qilinmaydi va yetkazib berilmaydi, uzr!</i>", parse_mode="html")

@dp.message_handler(text="ℹ️ Biz haqimizda", state='*')
async def about_section(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Dasturchi: @chogirmali_yigit\nKanal: @chogirmali_blog")

@dp.message_handler(text="⚙️ Sozlamalar", state='*')
async def get_settings(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Bu bo'lim hali tayyor emas")