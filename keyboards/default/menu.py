from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.row("đ Xarid qilish")
main.row("đ Savat", "đ Buyurtmalarim")
main.row("âī¸ Sozlamalar", "âšī¸ Biz haqimizda")

back_button = KeyboardButton(text="âŦī¸ Orqaga")
cart_button = KeyboardButton(text="đ Savat")

cats_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
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

def make_back_button(call_data):
    return InlineKeyboardButton(text="âŦī¸ Orqaga", callback_data=f"back_{call_data}")

def make_amount_markup(number=1):
    cart_button_inline = InlineKeyboardButton(text="đ Savatga qo'shish", callback_data=f"cart_{number}")
    markup = InlineKeyboardMarkup(row_width=3)
    add = InlineKeyboardButton(text="â", callback_data=f"add_{number}")
    remove = InlineKeyboardButton(text="â", callback_data=f"remove_{number}")
    button = InlineKeyboardButton(text=str(number), callback_data=str(number))
    markup.add(remove, button, add)
    markup.add(cart_button_inline)
    markup.add(make_back_button(call_data="amount"))
    return markup


phone_button = ReplyKeyboardMarkup(resize_keyboard=True)
phone_button.add(KeyboardButton(text="đ Telefon raqamni jo'natish", request_contact=True))

location_button = ReplyKeyboardMarkup(resize_keyboard=True)
location_button.add(KeyboardButton(text="đ Manzilni jo'natish", request_location=True))

confirm = InlineKeyboardMarkup(row_width=1)
confirm.add(InlineKeyboardButton(text="â Tasdiqlash â", callback_data="confirm_true"))
confirm.add(InlineKeyboardButton(text="â Bekor qilish â", callback_data="confirm_false"))
# confirm.add(InlineKeyboardButton(text="đ O'zgartirish đ", callback_data="confirm_retry"))


back_inline_button = InlineKeyboardButton(text="âŦī¸ Orqaga", callback_data="back")
cancel = InlineKeyboardButton(text="â Bekor qilish â", callback_data="cancel")

def payment_markup(payments):
    markup = InlineKeyboardMarkup(row_width=2)
    for payment in payments:
        markup.insert(InlineKeyboardButton(text=payment[1], callback_data=payment[1]))
    markup.row(cancel)
    markup.row(back_inline_button)
    return markup


