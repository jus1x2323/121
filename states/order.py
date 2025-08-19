from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    WAITING_USERNAME = State()
    WAITING_PAYMENT_PROOF = State()
    WAITING_STARS_COUNT = State()
    WAITING_GAME_ID = State()