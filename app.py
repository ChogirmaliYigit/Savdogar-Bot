from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Ma'lumotlar bazasini yaratamiz:
    # try:
    #     # db.create_table_users()
    #     # db.create_table_category()
    #     # db.create_product_table()
    #     # db.create_user_cart()
    #     # db.create_order_table()
    #     # db.create_order_item_table()
    #     db.create_payment_providers()
    # except Exception as err:
    #     print(err)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
