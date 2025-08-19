from aiogram.fsm.state import State, StatesGroup


class MSStates(StatesGroup):
    WAITING_USER_ID = State()
    WAITING_MEDIA = State()