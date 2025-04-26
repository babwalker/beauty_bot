from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    ru_mailing = State()
    en_mailing = State()
    de_mailing = State()
    get_media = State()