from aiogram.fsm.state import State, StatesGroup


class DesignRequestStates(StatesGroup):
    WAITING_VIDEO = State()