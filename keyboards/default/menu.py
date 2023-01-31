from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.row("🛍 Buyurtma berish")
main.row("🛒 Savat", "📋 Buyurtmalarim")
main.row("⚙️ Sozlamalar", "ℹ️ Biz haqimizda")

back_button = KeyboardButton(text="⬅️ Orqaga")
cart_button = KeyboardButton(text="🛒 Savat")

cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
cats = db.select_cats()
cats_markup.add(back_button, cart_button)
for cat in cats:
    cats_markup.insert(KeyboardButton(text=cat[1]))


def product_markup(products):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    markup.add(back_button, cart_button)
    for product in products:
        markup.insert(KeyboardButton(text=product[1]))
    return markup

back_button_inline = InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")

def make_amount_markup(number=1):
    cart_button_inline = InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"cart_{number}")
    markup = InlineKeyboardMarkup(row_width=3)
    add = InlineKeyboardButton(text="➕", callback_data=f"add_{number}")
    remove = InlineKeyboardButton(text="➖", callback_data=f"remove_{number}")
    button = InlineKeyboardButton(text=str(number), callback_data=str(number))
    markup.add(remove, button, add)
    markup.add(cart_button_inline)
    markup.add(back_button_inline)
    return markup