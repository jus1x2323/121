from aiogram.fsm.state import State, StatesGroup


class ScriptRequestStates(StatesGroup):
    WAITING_CONTACT = State()
    WAITING_SPEC = State()