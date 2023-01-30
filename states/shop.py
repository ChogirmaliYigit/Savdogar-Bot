from aiogram.dispatcher.filters.state import State, StatesGroup


class AllStates(StatesGroup):
    category = State()
    product = State()
    amount = State()

