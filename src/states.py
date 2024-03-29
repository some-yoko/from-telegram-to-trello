from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class NewTask(StatesGroup):
    """
    Class(Final State Machine) for creating new task

    """
    list = State()
    header = State()
    description = State()
    member = State()
    tags = State()
    deadline = State()
    position = State()
