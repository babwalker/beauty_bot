from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from user_router.states import Form
from user_router.utils.inline_buttons_data import PROCEDURES_FREQUENCY, SKIN_FEATURES, SKIN_TYPES
from user_router.utils.service import get_inline_text, get_text, show_progress
from config import Settings

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)

router = Router()

@router.callback_query(F.data == "other")
async def process_other(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    progress = await show_progress(state)

    if current_state == Form.gender.state:
        await callback.message.edit_text(
            f"{progress}\n\n{get_text(callback.from_user.id, 'gender_question')}",
            reply_markup=InlineKeyboardBuilder()
                .button(text=get_text(callback.from_user.id, "back_button"), callback_data="back_gender")
                .as_markup()
        )
        await state.set_state(Form.gender)

    elif current_state == Form.skin_problems.state:
        await callback.message.edit_text(
            f"{progress}\n\n{get_text(callback.from_user.id, 'other_skin_problems')}",
            reply_markup=InlineKeyboardBuilder()
                .button(text=get_text(callback.from_user.id, "back_button"), callback_data="back_skin_problems")
                .as_markup()
        )
        await state.set_state(Form.skin_problems)

    elif current_state == Form.daily_products.state:
        await callback.message.edit_text(
            f"{progress}\n\n{get_text(callback.from_user.id, 'other_daily_products')}",
            reply_markup=InlineKeyboardBuilder()
                .button(text=get_text(callback.from_user.id, "back_button"), callback_data="back_daily_products")
                .as_markup()
        )
        await state.set_state(Form.daily_products)

    await callback.answer()

@router.message(Form.gender)
async def save_other_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    progress = await show_progress(state)
    data = await state.get_data()
    message_id = data.get("prev_message")

    builder = InlineKeyboardBuilder()
    for key in SKIN_TYPES:
        builder.button(text=get_inline_text(message.from_user.id, "SKIN_TYPES", key), callback_data=f"skin_{key}")
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_gender")
    builder.adjust(2)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=f"{progress}\n\n{get_text(message.from_user.id, 'skin_type_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.skin_type)
    await message.delete()

@router.message(Form.skin_problems)
async def save_skin_other(message: types.Message, state: FSMContext):
    await state.update_data(skin_problems=[message.text])
    progress = await show_progress(state)
    data = await state.get_data()
    message_id = data.get("prev_message")

    builder = InlineKeyboardBuilder()
    for key in SKIN_FEATURES:
        builder.button(text=get_inline_text(message.from_user.id, "SKIN_FEATURES", key), callback_data=f"feature_{key}")
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_skin_problems")
    builder.adjust(2)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=f"{progress}\n\n{get_text(message.from_user.id, 'skin_features_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.skin_features)
    await message.delete()

@router.message(Form.daily_products)
async def save_products_other(message: types.Message, state: FSMContext):
    await state.update_data(daily_products=[message.text])
    progress = await show_progress(state)
    data = await state.get_data()
    message_id = data.get("prev_message")

    builder = InlineKeyboardBuilder()
    for key in PROCEDURES_FREQUENCY:
        builder.button(text=get_inline_text(message.from_user.id, "PROCEDURES_FREQUENCY", key), callback_data=f"procedure_{key}")
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_daily_products")
    builder.adjust(2)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=f"{progress}\n\n{get_text(message.from_user.id, 'procedures_frequency_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.procedures_frequency)
    await message.delete()