from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
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

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton(text="🛍 Buyurtma berish"))
main.add(KeyboardButton(text="🛒 Savatcha"), KeyboardButton(text="📂 Buyurtmalarim"))
main.add(KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="💰 Hamyonim"))

back_markup = KeyboardButton(text="⬅️ Orqaga")
cart_markup = KeyboardButton(text="🛒 Savatcha")

cat_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
cats = db.select_cats()
cat_markup.add(back_markup, cart_markup)
for cat in cats:
    cat_markup.insert(KeyboardButton(text=cat[1]))


def product_markup(products):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    markup.add(back_markup, cart_markup)
    for product in products:
        markup.insert(KeyboardButton(text=product[1]))
    return markup


back_markup_inline = InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")

def make_amount_markup(number=1):
    cart_markup_inline = InlineKeyboardButton(text="🛒 Savatchaga qo'shish", callback_data=f"cart_{number}")
    markup = InlineKeyboardMarkup(row_width=3)
    add = InlineKeyboardButton(text="➕", callback_data=f"add_{number}")
    remove = InlineKeyboardButton(text="➖", callback_data=f"remove_{number}")
    button = InlineKeyboardButton(text=str(number), callback_data=str(number))
    markup.add(remove, button, add)
    markup.add(cart_markup_inline)
    markup.add(back_markup_inline)
    return markup


def make_photo_viewer(link, id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Rasmni ko'rish", callback_data=id, web_app=WebAppInfo(url=link)))
    return markup


phone_button = ReplyKeyboardMarkup(resize_keyboard=True)
phone_button.add(KeyboardButton(text="📞 Telefon raqamni jo'natish", request_contact=True))

location_button = ReplyKeyboardMarkup(resize_keyboard=True)
location_button.add(KeyboardButton(text="📍 Manzilni jo'natish", request_location=True))

confirm = InlineKeyboardMarkup(row_width=1)
confirm.add(InlineKeyboardButton(text="✅ Tasdiqlash ✅", callback_data="confirm_true"))
confirm.add(InlineKeyboardButton(text="🔁 O'zgartirish 🔁", callback_data="confirm_retry"))
confirm.add(InlineKeyboardButton(text="❌ Bekor qilish ❌", callback_data="confirm_false"))


payment_markup = InlineKeyboardMarkup(row_width=2)
payment_markup.row(InlineKeyboardButton(text="💵 Naqd pul", callback_data="naqd"), InlineKeyboardButton(text="💳 Click", callback_data="click"))
payment_markup.row(InlineKeyboardButton(text="💳 Payme", callback_data="payme"), InlineKeyboardButton(text="💳 Visa", callback_data="visa"))
payment_markup.add(back_markup_inline)


