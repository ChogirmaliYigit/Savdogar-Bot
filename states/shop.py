from aiogram.dispatcher.filters.state import State, StatesGroup


class AllStates(StatesGroup):
    category = State()
    product = State()
    amount = State()
    cart = State()
    order_note = State()
    get_phone = State()
    get_address = State()
    order_confirm = State()
    paid_state = State()


class AdminStates(StatesGroup):
    add_title = State()
    add_token = State()