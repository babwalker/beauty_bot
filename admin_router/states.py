from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    ru_mailing = State()
    ru_media = State()

    en_mailing = State()
    en_media = State()

    de_mailing = State()
    de_media = State()