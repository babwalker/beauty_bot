from aiogram.fsm.state import StatesGroup, State

# States
class Form(StatesGroup):
    name = State()
    country = State()
    email = State()
    age = State()
    gender = State()
    skin_type = State()
    skin_problems = State()
    skin_features = State()
    lifestyle = State()
    water_intake = State()
    daily_products = State() 
    procedures_frequency = State()
    photo_full_face = State()
    photo_right_profile_face = State()
    photo_left_side_face = State()
    budget = State()
    composition_preferences = State()