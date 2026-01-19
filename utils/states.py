"""
FSM States for user registration
"""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for user registration process"""
    waiting_for_phone = State()
    waiting_for_name = State()


class TestStates(StatesGroup):
    """States for test process"""
    in_progress = State()
