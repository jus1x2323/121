from aiogram.fsm.state import State, StatesGroup


class CartStates(StatesGroup):
    WAITING_ITEM_INDICES = State()
    WAITING_ITEM_TO_EDIT = State()
    WAITING_EDIT_ACTION = State()
    WAITING_NEW_QUANTITY = State()